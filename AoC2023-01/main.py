# Imports string data line by line
data = [ line.rstrip() for line in open( 'input.dat', 'r' ) ]

string_digits = { 1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine' }

def find_digits(word):
  digits = {}
  for n, character in enumerate(word):
    if character.isdigit():
      digits[n] = int(character)
  for digit in string_digits:
    result = 0
    while True:
      result = word.find( string_digits[digit], result)
      if result > -1:
        digits[result] = digit
        result = result + 1
      else:
        break
  return digits

def find_number(word):
  digit_idx = find_digits(word)
  return digit_idx[max(digit_idx.keys())] + 10*digit_idx[min(digit_idx.keys())]

numbers = [ find_number(word) for word in data]

print( sum(numbers) )