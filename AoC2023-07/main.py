def convert_labels_to_values(labels):
  values = []
  for label in labels:
    if label == 'A':
      values.append(14)
    elif label == 'K':
      values.append(13)
    elif label == 'Q':
      values.append(12)
    elif label == 'J':
      values.append(1)
    elif label == 'T':
      values.append(10)
    else:
      values.append(int(label))
  return values

def determine_type(values):
  freq = {}
  for v in values:
    freq[v] = values.count(v)

  # Joker present
  if 1 in freq:
    if len(freq) <= 2:
      # Five or four jokers
      return 6
    if freq[1] == 3:
      # Four of a kind with three jokers
      return 5
    if freq[1] == 2 and len(freq) == 3:
      # Four of a kind with two jokers
      return 5
    if freq[1] == 2:
      # Three of a kind with two jokers
      return 3
    # One joker
    if len(freq) == 3 and 2 in freq.values():
      # Full house with one joker
      return 4
    if len(freq) == 3:
      # Four of a kind with one joker
      return 5
    if len(freq) == 4:
      # Three of a kind with one joker
      return 3
    return 1
    
  # Five of a kind
  if len(freq) == 1:
    return 6
  elif len(freq) == 2:
    # Four of a kind
    if 1 in freq.values():
      return 5
    # Full house
    else:
      return 4
  elif len(freq) == 3:
    # Three of a kind
    if 3 in freq.values():
      return 3
    # Two pair
    else:
      return 2
  # One pair
  elif len(freq) == 4:
    return 1
  # High Card
  else:
    return 0

class CamelHand:
    def __init__(self, c, b):
      self.card_labels = c
      self.card_values = convert_labels_to_values(c)
      self.bid = b
      self.type = determine_type(self.card_values)
    def __repr__(self):
      return 'Cards: {}, Bid: {}, Type: {}'.format(self.card_labels, self.bid, self.type)
    def __eq__(self,other):
      return self.card_labels == other.card_labels and self.bid == other.bid
    def __lt__(self,other):
      if self.type != other.type:
        return self.type < other.type
      else:
        return self.card_values < other.card_values

# Imports string data line by line
data = [line.rstrip().split() for line in open('input.dat', 'r')]
hands = sorted([ CamelHand( h[0], int(h[1]) ) for h in data ])

winnings = 0
for rank, hand in enumerate(hands):
  print(hand)
  winnings += (rank+1) * hand.bid

print(winnings)