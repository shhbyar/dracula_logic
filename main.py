from enum import Enum
import random
import os

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
  def __init__(self, color: Colors, value):
    self.color = color
    self.value = value
    self.c = Colors(color).name
    self.rev = False
    
class Player():
  def __init__(self, _type:_Type):
    self._type = _type
    self.cards, self.deck = ([],)*2
    self.hp = 12
    self.revealed_cards = list()
    self.has_revealed_card = False
    self.name = str.title(_Type(self._type).name)
    
  def reveal(self, index: int):
    self.cards[index].rev = True
    self.revealed_cards.append({0: self.cards[index], 1: index+1})
    self.has_revealed_card = True
    pass
  
  def fold_all(self):
    for card in self.cards: card.rev = False
    del(self.revealed_cards[:])
    
  def swap(self, first: int, sec: int):
    self.cards[first], self.cards[sec] = self.cards[sec], self.cards[first]
    
  def trade(self, index: int, opponent):
    self.cards[index], opponent.cards[index] = opponent.cards[index], self.cards[index]
    pass

# :Pre game
dracula_hp = 12
people = [ 4 ]*5

color_ranking = list( range(0,4) )
random.shuffle(color_ranking)

discard_pile = []

init_stack:list = []
for i in range(0,4):
  for j in range(1,9):
    init_stack.append(Card(i, j))

card_stack = init_stack
random.shuffle(card_stack)

dracula = Player(_Type.DRACULA)
van = Player(_Type.VAN_HELSING)
# End of :Pre game

# Game Starts:
con()
print(f"The Trump Color is \"{Colors(color_ranking[0]).name.title()}\"")
con()

# loop for rounds
for r in range(5):
  
  dracula.cards = card_stack[-5:]
  del card_stack[-5:]

  van.cards = card_stack[-5:]
  del card_stack[-5:]
  
  print(f"Round {r+1} has started")
  print("Alive:", people)
  
  con()
  
  player, opponent = van, dracula
  
  # :a loop for turns
  while (True):
    
    # Switch player each turn
    player, opponent = opponent, player
    
    cl()
    print(f"It's {player.name}'s turn!\n\n")
    print(f"Cards in your tray:\n {list(map(lambda card: f"{card.c} {card.value}{" REVEALED" if card.rev else "" }", player.cards))}")
    
    if opponent.has_revealed_card: 
      print(f"{opponent.name}'s revealed cards: {list(map(lambda card: f"{card[0].c} {card[0].value} in District {card[1]}", opponent.revealed_cards))}")
      
    if player.has_revealed_card: 
      print(f"Your's revealed cards: {list(map(lambda card: f"{card[0].c} {card[0].value} in District {card[1]}", player.revealed_cards))}")

    drawn_card = card_stack.pop()
    print(f"The drawn card is \"{drawn_card.c} {drawn_card.value}\"\n")
    print("What will it be?\n1. Dismiss\n2. Replace\n\n")

    inp = int(input())
    match inp:
      case 1:
        match 7:#drawn_card.value:
          case 1:
            # Reveal one of your cards.
            print("Choose a district to reveal:")
            inp = int(input())
            player.reveal(inp-1)
            
          case 2:
            # Reveal the top card of the deck.
            print(f"The next card is {card_stack[-1]}")
            
          case 3:
            print("Choose a district to reveal your opponent's card:")
            inp = int(input())
            opponent.reveal(inp-1)
            
          case 4:
            # Swap two of your cards
            print("Choose the first district to swap:")
            print(f"Cards in your tray: "+
                  {list(map(lambda card: f"{card.c} {card.value}", player.cards))})
            first = int(input())
            
            print("Choose the second district to swap:")
            print(f"Cards in your tray: " +
                  {list(map(lambda card: f"{card.c} {card.value}", player.cards))})
            sec = int(input())
            
            player.swap(first-1, sec-1)
            
          case 5:
            # Play another turn. This effect applies even if your
            # opponent has called the end of the round on their turn.
            print("sakht shod ke baba :(")
            
          case 6:
            # Swap (trade) one of your cards with your opponent.
            # Both cards must face the same District.
            print("Choose the second district to trade:")
            district = int(input())
            player.trade(district-1, opponent)
            pass
          
          case 7:
            # Swap the Trump Color Token with another Color Token
            print(f"The current Trump Color is {Colors(color_ranking[0]).name}\n"+
                  f"Other colors in order:")
            for i, color in enumerate(color_ranking[1:]):
              print(f"{i+1}. {Colors(color).name}")
            print("\nWhats the new Trump Color?")
            new_trump = int(input())
            color_ranking[0], color_ranking[new_trump-1] = color_ranking[new_trump-1], color_ranking[0]

          case 8:
            # You can’t discard an 8 unless there are at least 6 cards in 
            # the discard pile. Immediately end the round. 
            # Your opponent does not play their turn.
            if len(discard_pile) > 5:
              break

      case 2:
        pass # :Replace
      
      case 3:
        last_turn = True
        continue
    break
  
  
  print(f"Round {r+1} has finished")
  card_stack = init_stack[:]
  random.shuffle(card_stack)
  
else:
  print("All rounds are finished without Van-Helsing winning... so: Dracula Wins!!")
