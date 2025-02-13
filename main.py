from enum import Enum
import random

class Colors(Enum):
  RED = 0
  BLUE = 1
  PURPLE = 2
  YELLOW = 3
  
class Card():
  def __init__(self, color: Colors, value):
    self.color = color
    self.value = value


# :Pre game
dracula_hp = 12
people = [ list( range(1,5) ) ] * 5

color_ranking = list( range(0,4) )
random.shuffle(color_ranking)

hokm = color_ranking[-1]
discard_pile = []

card_stack:list = []
for i in range(0,4):
  for j in range(0,8):
    card_stack.append(Card(i, j+1))
random.shuffle(card_stack)
# End of :Pre game

print(f"The Trump Color is \"{Colors(hokm).name.title()}\"")
for r in range(5):
  
  dracula_cards = card_stack[-5:]
  del card_stack[-5:]

  van_helsing = card_stack[-5:]
  del card_stack[-5:]
  
  
  print(f"Round {r+1} has started")
  print("Alive:", people)
  while (True):
    break
  print(f"Round {r+1} has finished")
