from enum import Enum
import random

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
    
class Player():
  def __init__(self, _type:_Type):
    self._type = _type
    self.cards, self.deck, self.tray = ([],)*3
    self.hp = 12


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

print(f"The Trump Color is \"{Colors(color_ranking[0]).name.title()}\"")

# loop for rounds
for r in range(5):
  
  dracula.cards = card_stack[-5:]
  del card_stack[-5:]

  van.cards = card_stack[-5:]
  del card_stack[-5:]
  
  print(f"Round {r+1} has started")
  print("Alive:", people)
  
  # :a loop for turns
  while (True):
    # Dracula's turn
    print("It's dracula's turn!")
    print(f"Cards in your tray: {list(map(lambda card: f"{card.c} {card.value}", dracula.cards))}")
    print(f"Cards in your dock: {list(map(lambda card: f"{card.c} {card.value}", dracula.deck))}")
    drawn_card = card_stack.pop()
    print(f"The drawn card is {drawn_card.c} {drawn_card.value}")
    print("What will it be?\n1. Dismiss\n2. Replace")
    inp = input()
    if (inp == "1"):
      match drawn_card.value:
        case 1:
          print("Choose a card to reveal:")
          print(f"Cards in your tray: {list(map(lambda card: f"{card.c} {card.value}", dracula.cards))}")
          inp = input()
          
        case 2:
          print(f"The next card is {card_stack[-1]}")
          
        case 3:
          print("Choose a card to reveal:")
          print(f"Cards in your tray: {list(map(lambda card: f"{card.c} {card.value}", van.cards))}")
          inp = input()
          
        case 4:
          # Swap two of your cards
          print("Choose a card to swap:")
          print(f"Cards in your tray: {list(map(lambda card: f"{card.c} {card.value}", dracula.cards))}")
          inp = input()
          
        case 5:
          print("sakht shod ke baba :(")
          
        case 6:
          # Swap one of your cards with your opponent.
          # Both cards must face the same District.
          pass
        
        case 7:
          # Swap the Trump Color Token with another Color Token
          print("Whats the new Trump Color?")
          inp = input()
          
        case 8:
          if len(discard_pile) > 5:
            break
          

    elif (inp == "2"):
      pass # :Replace
    break
  
  
  print(f"Round {r+1} has finished")
  card_stack = init_stack[:]
  random.shuffle(card_stack)
  
else:
  print("All rounds are finished without Van-Helsing winning... so: Dracula Wins!!")
