from enum import Enum
import random
import os
from time import sleep

os.system("mode con: cols=80 lines=30") 
sleep(1)

def cl():
  os.system("cls")
  
def con():
  input("\n\n\n\nPress Enter to continue...")
  cl()

class Colors(Enum):
  RED = 0
  BLUE = 1
  PURPLE = 2
  YELLOW = 3
  GREEN = 4
  
class _Type(Enum):
  DRACULA = 0
  VAN_HELSING = 1
  
  
class Card():
  def __init__( self, color: Colors, value: int ):
    # Initialize a card with a color and value
    
    self.color = color
    self.value = value
    self.c = str.title( Colors( color ).name )
    self.rev = False
    
  def view( self ) -> str:
    # Return a string representation of the card with color formatting
    
    text = colorify( f"{ str( self.value ) } { self.c }", self.color )
    return text
  
def colorify( text: str, color: Colors ):
  
  if type(color) == int:
    color = Colors(color)

  _end : str = "\033[00m"
  style : str = ""

  match color:
    case Colors.RED: # RED
      style = "\033[91m"
    
    case Colors.GREEN: # GREEN
      style = "\033[92m"
      
    case Colors.YELLOW: # YELLOW
      style = "\033[93m"

    case Colors.BLUE: # BLUE
      style = "\033[94m"

    case Colors.PURPLE: # PURPLE
      style = "\033[95m"
    
    case _:
      style = "\033[93m"
    
  return f"{style}{text}{_end}"
    
class Player():
  def __init__(self, _type:_Type):
    self._type = _type
    self.cards, self.deck = ([],) * 2
    self.hp = 12
    self.has_revealed_card = False
    self.name = str.title(_Type(self._type).name)
    self.revealed_districts = []
    
  def view_cards( self ) -> str:
    text = ""
    for i, card in enumerate( self.cards ):
      text += f"{ str.upper( chr( i + ord( "a" ) ) ) }. { card.view() }\n"
    return text
  
  def view_revealed( self ) -> str:
    if not self.has_revealed_card:
      return "No cards have been revealed yet."
    text = ""
    for i in self.revealed_districts:
      text += f"In District { i + 1 }, { self.cards[i].view() } was revealed."
    return text

  def reveal(self, index: int):
    # Should save revealed district not the card!
    self.revealed_districts.append(index)
    self.cards[index].rev = True
    self.has_revealed_card = True
  
  def fold_all(self):
    for card in self.cards: card.rev = False
    del(self.revealed_cards[:])
    
  def swap(self, first: int, sec: int):
    self.cards[first], self.cards[sec] = self.cards[sec], self.cards[first]
    
  def trade(self, index: int, opponent):
    self.cards[index], opponent.cards[index] = opponent.cards[index], self.cards[index]
  
  
class Game():
  class ColorRanking():
    
    def __init__(self):

      self.colors = list( range( 0, 4 ) )
      random.shuffle( self.colors )
      
    def view( self ) -> str:
      text = f"The current Trump Color is: \"{self.get_trump()}\"\n"
      text += "Other colors in order:\n"
      for i, color in enumerate( self.colors[1:] ):
        text += f"{ i + 1 }. { str.title( Colors( color ).name ) }\n"
      return text
      
    def get_trump( self ) -> str:
      color_name = str.title( Colors( self.colors[0] ).name )
      return colorify( color_name, Colors( self.colors[0] ) )
    
    def get_trump_color( self ) -> Colors:
      return Colors(self.colors[0])
    
    def get( self, index: int ) -> str:
      return str.title( Colors( self.colors[index] ).name )
    
    def new_trump( self, new_trump: int ):
      self.colors[0], self.colors[ new_trump - 1 ] = self.colors[ new_trump - 1 ], self.colors[0]

  def __init__( self ):
    self.stat : bool = False # Whether the game has started.
    self.rounds = 0
    self.dracula = Player( _Type.DRACULA )
    self.van = Player( _Type.VAN_HELSING )
    self.people = [ 4 ] * 5
    self.color_ranking = self.ColorRanking()
    self.discard_pile = []
    self.init_stack : list[Card] = []
    for i in range( 0, 4 ):
      for j in range( 1, 9 ):
        self.init_stack.append( Card( i, j ) )
    self.card_stack = []
    
  def start( self ):
    self.prompt( "Hello and welcome!" )

    for r in range( 5 ):
      # Things that happen each round
      self.rounds = r + 1
      
      self.card_stack.clear()
      self.card_stack.extend( self.init_stack )
      random.shuffle(self.card_stack)
  
      self.dracula.cards = self.card_stack[ :5 ]
      del self.card_stack[ :5 ]
      
      self.van.cards = self.card_stack[ :5 ]
      del self.card_stack[ :5 ]
      
      self.player, self.opponent = self.van, self.dracula
      
      while True:
        fin = self.turn()
        if fin == 1:
          self.turn()
          break
        if self.card_stack == []:
          self.prompt( "End of the round!" )
          break
      
      self.prompt( "End of the round!" )
      win = self.check_win()
      
      if win == 1:
        self.rounds = 0
        self.prompt( "Dracula won this game!" )
        break
      elif win == 2:
        self.rounds = 0
        self.prompt( "Van-Helsing won this game!" )
        break
    
    self.rounds = 0
    self.prompt( "All rounds are finished without Van-Helsing winning... so: Dracula Wins!!" )
  
  def check_win( self ) -> int:
    # Checks whether anyone has won
    # 0: No onw has won yet
    # 1: Dracula has won
    # 2: Van-Helsing has won

    # check decks, one by one
    for i in range(5):
      dracula_wins = False 
      text = f"Checking district {i+1}\nPeople Alive: {self.people[i]}\n"
      dracula_card: Card = self.dracula.cards[i]
      text += f"Dracula's card: {dracula_card.view()}\n"
      van_card: Card = self.van.cards[i]
      text += f"Van-Helsing's card: {van_card.view()}\n"
      trump_color = self.color_ranking.get_trump_color()
      # check if one of the cards is trump and the other is not:
      if ( dracula_card.color == van_card.color ):
        dracula_wins = True if dracula_card.value > van_card.value else False
      elif dracula_card.color == trump_color:
        dracula_wins = True
      elif van_card.color == trump_color:
        dracula_wins = False
      elif dracula_card.value == van_card.value:
        dracula_index = self.color_ranking.colors.index(dracula_card.color)
        van_index = self.color_ranking.colors.index(dracula_card.color)
        dracula_wins = True if dracula_index > van_index else False
      else:
        dracula_wins = True if dracula_card.value > van_card.value else False
      
      if dracula_wins:
        text += "Dracula wins in this district!\n"
        self.people[i] -= 1
      else:
        text += "Van-Helsing wins in this district!\n"
        self.dracula.hp -= 1
      
      self.prompt(text)
      
      if self.dracula.hp == 0:
        self.prompt("Van-Helsing wins!")
        return 2
      elif any( people == 0 for people in self.people ):
        self.prompt("Dracula wins!")
        return 1

    return 0  
  
  def turn( self, switch: bool | None = True ) -> bool:
    # Things that happen each turn
    
    self.player, self.opponent = ( self.opponent, self.player ) if switch else ( self.player, self.opponent )
    
    pro = f"It's { self.player.name }'s turn!\n"
    pro += f"Cards in your tray:\n{ self.player.view_cards() }\n"
    drawn_card = self.card_stack.pop()
    pro += f"The drawn card is: \"{drawn_card.view()}\"\n\n"
    pro += f"What will it be?\n{colorify( "1. Dismiss\n", Colors.GREEN ) }{colorify( "2. Replace\n", Colors.BLUE )}{colorify( "3. End Game\n", Colors.RED )}"

    choice: int = self.ask( pro )
    
    match choice:
      case 1:
        self.dismiss( drawn_card )
      case 2:
        self.replace( drawn_card )
      case 3:
        return 1 # End the round
      
      
  def dismiss( self, drawn_card: Card ):
    match drawn_card.value:
      case 1:
        # Reveal one of your cards.
        inp = self.ask("Choose a district to reveal:")
        self.player.reveal(inp-1)
        
      case 2:
        # Reveal the top card of the deck.
        self.prompt(f"The next card is {self.card_stack[-1].view()}")
        
      case 3:
        inp = self.ask("Choose a district to reveal your opponent's card:")
        self.opponent.reveal(inp-1)
        
      case 4:
        # Swap two of your cards
        first = self.ask(f"""Choose the first district to swap:
Cards in your tray:\n{self.player.view_cards()}""")
        
        sec = self.ask(f"""Choose the second district to swap:
Cards in your tray:\n{self.player.view_cards()}""")

        self.player.swap(first-1, sec-1)

      case 5:
        # Play another turn. This effect applies even if your
        # opponent has called the end of the round on their turn.
        self.turn( False )
        
      case 6:
        # Swap (trade) one of your cards with your opponent.
        # Both cards must face the same District.
        district = self.ask("Choose the district to trade:")
        self.player.trade(district-1, self.opponent)
      
      case 7:
        # Swap the Trump Color Token with another Color Token
        self.prompt( self.color_ranking.view() )
        new_trump = self.ask( "Whats the new Trump Color?" )
        self.color_ranking.new_trump( new_trump )

      case 8:
        # You can’t discard an 8 unless there are at least 6 cards in 
        # the discard pile. Immediately end the round. 
        # Your opponent does not play their turn.
        if len(self.discard_pile) > 5:
          pass

    self.discard_pile.append(drawn_card)
    
  def replace( self, drawn_card: Card ):
    pro = f"Which card will you replace?\n"
    pro += f"{self.player.view_cards()}"
    choice = self.ask(pro)
    self.dismiss(self.player.cards[choice-1])
    self.player.cards[choice-1] = drawn_card

  def brief( self ) -> str:
    # Gives a brief report of game state
    # returns str

    final = ""
    if self.rounds > 0:
      final += colorify( f"Round {self.rounds}\n", Colors.BLUE )
      final += f"The Trump Color is \"{self.color_ranking.get_trump()}\"\n"
      final += colorify( f"Dracula's HP: {self.dracula.hp}\n\n", Colors.RED )
      final += f"Alive: {self.people}\n"
      final += f"Van's revealed cards: {self.van.view_revealed()}\n"
      final += f"Dracula's revealed cards: {self.dracula.view_revealed()}\n"
      final += f"cards left in stack: {len(self.card_stack)}\n"
      final += "\n___________________________\n\n"
      
      
      # if self.pla
    else:
      final = "Game hasn't started yet!\n___________________________\n\n"
    
    return final

  def write( self, text: str ):
    columns, lines = os.get_terminal_size()
    _out: str = ""
    _out += text
    
    line_count = text.count( "\n" ) + 1
    
    for _ in range( 0, lines - line_count - 1 ):
      _out += "\n"
    
    
    print( _out, end = "" )
    
    
  def ask ( 
    self,
    text: str,
    query: str | None = "Enter the number and press Enter: "
  ) -> int:
    # Asks the given query and returns the number
    # user inputs
    self.clear()
    brief = self.brief()
    self.write( brief + text )
    
    print( query, end = "" )
    try:
      _in = int(input())
    except ValueError:
      self.ask(
        text,
        colorify(
          "You should enter a number! Please enter a valid number this time:",
          Colors.RED
          )
      )
    return _in
  
  def prompt( self, text: str ):
    
    self.clear()
    brief = self.brief()
    self.write( brief + text )
    print( "\rPress Enter to continue...", end = "" )
    input()
    
  def clear( self ):
    os.system( "cls" )
    
  

game = Game()
game.start()
