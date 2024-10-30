# Imports string data line by line
data = [line.rstrip().split(':') for line in open('input.dat', 'r')]

cards={}
for card_data, number_data in data:
  card = int(card_data[5:])
  winners, numbers = (set(nums.split()) for nums in number_data.split('|'))
  cards[card]=[1,winners,numbers]

for card_number, [copies, wins, nums] in cards.items():
  matches = len(wins.intersection(nums))
  for i in range(card_number+1, card_number+matches+1):
    cards[i][0] += copies

sum = 0
for x in cards.values():
  sum += x[0]

print(sum)