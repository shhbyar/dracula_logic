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
  
class _Type(Enum):
  DRACULA = 0
  VAN_HELSING = 1
  
class Card():
  def __init__( self, color: Colors, value ):
    # Initialize a card with a color and value
    
    self.color = color
    self.value = value
    self.c = Colors( color ).name
    self.rev = False
    
  def view( self ):
    # Return a string representation of the card with color formatting
    
    # Should Use colorify method!!!!!
    
    _end : str = "\033[00m"
    color : str = ""

    match self.value:
      case 0: # RED
        color = "\033[91m"

      case 1: # BLUE
        color = "\033[94m"

      case 2: # PURPLE
        color = "\033[95m"
        
      case 3: # YELLOW
        color = "\033[93m"
      
    return f"{color}{self.c}{self.value}{_end}"
  
def colorify( text: str, color: Colors ):

  _end : str = "\033[00m"
  color : str = ""

  match color:
    case Colors.RED: # RED
      color = "\033[91m"

    case Colors.BLUE: # BLUE
      color = "\033[94m"

    case Colors.PURPLE: # PURPLE
      color = "\033[95m"
      
    case Colors.YELLOW: # YELLOW
      color = "\033[93m"
    
  return f"{color}{text}{_end}"
    
class Player():
  def __init__(self, _type:_Type):
    self._type = _type
    self.cards, self.deck = ([],) * 2
    self.hp = 12
    self.revealed_cards = list()
    self.has_revealed_card = False
    self.name = str.title(_Type(self._type).name)
     
  def reveal(self, index: int):
    self.cards[index].rev = True
    self.revealed_cards.append({0: self.cards[index], 1: index+1})
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
      
    def get_trump( self ) -> str:
      return str.title( Colors( self.colors[0] ).name )
    
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
    self.color_ranking = list( range( 0, 4 ) )
    self.discard_pile = []
    self.init_stack : list[Card] = []
    for i in range( 0, 4 ):
      for j in range( 1, 9 ):
        self.init_stack.append( Card( i, j ) )
    self.card_stack = self.init_stack
    
    random.shuffle(self.color_ranking)
    random.shuffle(self.card_stack)
    
  def start( self ):
    self.prompt( "Hello and welcome!" )

    for r in range( 5 ):
      self.rounds = r
      self.round()
    
    self.rounds = 0
    print( "All rounds are finished without Van-Helsing winning... so: Dracula Wins!!" )
  
  def check_win( self ) -> int:
    # Checks whether anyone has won
    # 0: No onw has won yet
    # 1: Dracula has won
    # 2: Van-Helsing has won
    
    if self.dracula.hp == 0: 
      return 2
  
    return 0  
  
  def round( self ):
    # Things that happen each round
    
    self.dracula.cards = self.card_stack[ -5: ]
    del self.card_stack[ -5: ]
    
    self.van.cards = self.card_stack[ -5: ]
    del self.card_stack[ -5: ]
    
    switch = True
    self.prompt( "Hello and welcome!" )

    while True:
      # Each turn
      player, opponent = ( self.van, self.dracula ) if switch else ( self.dracula, self.van )
      
      self.cl()
      op_cards = list( map( lambda card: f"{ card[0].c } { card[0].value } in District { card[1]} ", opponent.revealed_cards ) ) if opponent.has_revealed_card else ""
      
      self.prompt( f"""It's { player.name }'s turn!\n""" )

  def brief( self ) -> str:
    # Gives a brief report of game state
    # returns str

    final = ""
    if self.rounds > 0:
      final += colorify( f"Round {self.round}\n\n", Colors.BLUE )
      final += f"Alive: {self.people}\n"
      final += f"The Trump Color is \"{Colors(self.color_ranking[0]).name.title()}\"\n"
      final += colorify( f"Dracula's HP: {self.dracula.hp}\n\n", Colors.RED )
      final += "\n___________________________\n"
    else:
      final = "Game hasn't started yet!"
    
    return final

  def write( self, text: str ):
    columns, lines = os.get_terminal_size()
    _out: str = ""
    _out += text
    
    line_count = text.count( "\n" ) + 1
    
    for _ in range( 0, lines - line_count ):
      _out += "\n"
    
    
    print( _out, end = "" )
    
    
  def ask ( 
    self,
    text: str,
    query: str | None = "Enter the number and press Enter: "
  ) -> int:
    # Asks the given query and returns the number
    # user inputs
    
    self.write( text ) 
    
    print( query, end = "" )
    try:
      _in = int(input())
    except( NotImplemented ):
      self.ask(
        text,
        colorify(
          str + "\n\nYou should enter a number!",
          Colors.RED
          )
      )
    return _in
  
  def prompt( self, text: str ):
    
    self.clear()
    brief = self.brief()
    self.write( brief + text )
    print( "\nPress Enter to continue...", end = "" )
    input()
    
  def clear( self ):
    os.system( "cls" )

game = Game()

game.start()

# # :Pre game operation
# dracula_hp = 12
# people = [ 4 ]*5

# color_ranking = list( range(0,4) )
# random.shuffle(color_ranking)

# discard_pile = []

# init_stack:list = []
# for i in range(0,4):
#   for j in range(1,9):
#     init_stack.append(Card(i, j))

# card_stack = init_stack
# random.shuffle(card_stack)

# dracula = Player(_Type.DRACULA)
# van = Player(_Type.VAN_HELSING)
# # End of :Pre game

# # Game Starts:

# # loop for rounds
# for r in range(5):
  
#   def prompt(prompt: str):
#   # Gives a brief summery of current situation of thr game
#     brief = f"""Round \033[91m {r+1}\033[00m
# Alive: \033[96m {people}\033[00m
# The Trump Color is \"{Colors(color_ranking[0]).name.title()}\""""
    
#     cl()
#     size = { 0: os.get_terminal_size().lines, 1: os.get_terminal_size().columns }
#     con = str(brief+"\n___________________________\n"+prompt)
#     line_count = con.count("\n") + 1
    
    
#     print(con, end="")
#     ns = ""
#     for _ in range(0, size[0] - line_count):
#       ns += "\n"
#     print(ns + "\nPress Enter to continue...", end="")
#     input()
  
#   dracula.cards = card_stack[-5:]
#   del card_stack[-5:]

#   van.cards = card_stack[-5:]
#   del card_stack[-5:]
    
#   switch = True
#   prompt("Hello and welcome!")
#   # :a loop for turns
#   while (True):
    
#     # Switch player each turn
#     player, opponent = (van, dracula) if switch else (dracula, van)
    
#     cl()
#     op_cards = list(map(lambda card: f"{card[0].c} {card[0].value} in District {card[1]}", opponent.revealed_cards)) if opponent.has_revealed_card else ""

#     prompt(f"""It's {player.name}'s turn!\n
# Cards in your tray:
# {list(map(lambda card: f"{card.c} {card.value}{" REVEALED" if card.rev else "" }", player.cards))}
# {op_cards}"""
# )
#     input()
#     if opponent.has_revealed_card: 
#       print(f"Your's revealed cards: {list(map(lambda card: f"{card[0].c} {card[0].value} in District {card[1]}", player.revealed_cards))}")

#     drawn_card = card_stack.pop()
#     print(f"The drawn card is \"{drawn_card.c} {drawn_card.value}\"\n")
#     print("What will it be?\n1. Dismiss\n2. Replace\n\n")

#     inp = int(input())
#     match inp:
#       case 1:
#         match 7:#drawn_card.value:
#           case 1:
#             # Reveal one of your cards.
#             print("Choose a district to reveal:")
#             inp = int(input())
#             player.reveal(inp-1)
            
#           case 2:
#             # Reveal the top card of the deck.
#             print(f"The next card is {card_stack[-1]}")
            
#           case 3:
#             print("Choose a district to reveal your opponent's card:")
#             inp = int(input())
#             opponent.reveal(inp-1)
            
#           case 4:
#             # Swap two of your cards
#             print("Choose the first district to swap:")
#             print(f"Cards in your tray: "+
#                   {list(map(lambda card: f"{card.c} {card.value}", player.cards))})
#             first = int(input())
            
#             print("Choose the second district to swap:")
#             print(f"Cards in your tray: " +
#                   {list(map(lambda card: f"{card.c} {card.value}", player.cards))})
#             sec = int(input())
            
#             player.swap(first-1, sec-1)
            
#           case 5:
#             # Play another turn. This effect applies even if your
#             # opponent has called the end of the round on their turn.
#             print("sakht shod ke baba :(")
            
#           case 6:
#             # Swap (trade) one of your cards with your opponent.
#             # Both cards must face the same District.
#             print("Choose the second district to trade:")
#             district = int(input())
#             player.trade(district-1, opponent)
#             pass
          
#           case 7:
#             # Swap the Trump Color Token with another Color Token
#             print(f"The current Trump Color is {Colors(color_ranking[0]).name}\n"+
#                   f"Other colors in order:")
#             for i, color in enumerate(color_ranking[1:]):
#               print(f"{i+1}. {Colors(color).name}")
#             print("\nWhats the new Trump Color?")
#             new_trump = int(input())
#             color_ranking[0], color_ranking[new_trump-1] = color_ranking[new_trump-1], color_ranking[0]

#           case 8:
#             # You can’t discard an 8 unless there are at least 6 cards in 
#             # the discard pile. Immediately end the round. 
#             # Your opponent does not play their turn.
#             if len(discard_pile) > 5:
#               break

#       case 2:
#         pass # :Replace
      
#       case 3:
#         last_turn = True
#         continue
#     break
  
  
#   print(f"Round {r+1} has finished")
#   card_stack = init_stack[:]
#   random.shuffle(card_stack)
  
# else:
#   print("All rounds are finished without Van-Helsing winning... so: Dracula Wins!!")
