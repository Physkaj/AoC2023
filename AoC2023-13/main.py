def arrange_data(data):
  datasets = []
  dataset = []
  for row in data:
    if row:
      dataset.append(row)
    else:
      datasets.append(dataset)
      dataset = []
  datasets.append(dataset)
  return datasets
  
def load_data( file_name ):
  with open(file_name,'r') as file:
    data = [ list(line.strip()) for line in file]
  return arrange_data(data)

def rows_eq( i1, i2, matrix):
  errs = 0
  for x1, x2 in zip(matrix[i1],matrix[i2],strict=False):
    errs += 0 if x1 == x2 else 1
  return errs

def cols_eq( i1, i2, matrix):
  errs = 0
  for r in matrix:
    errs += 0 if r[i1] == r[i2] else 1
  return errs

# Mirror line is assumed to be to the right of the column index
def is_vertical_mirror_line(i1, matrix):
  i2 = i1+1
  errs = 0
  while i1 >= 0 and i2 < len(matrix[0]) and errs <= 1:
    errs += cols_eq(i1,i2,matrix)
    i1 -= 1
    i2 += 1
  return errs == 1

# Mirror line is assumed to be below the row index
def is_horizontal_mirror_line(i1, matrix):
  i2 = i1+1
  errs = 0
  while i1 >= 0 and i2 < len(matrix) and errs <= 1:
    errs += rows_eq(i1,i2,matrix)
    i1 -= 1
    i2 += 1
  return errs == 1

def find_horizontal_mirror_line(matrix):
  for i in range(0,len(matrix)-1):
    if is_horizontal_mirror_line(i,matrix):
      return i
  return -1

def find_vertical_mirror_line(matrix):
  for i in range(0,len(matrix[0])-1):
    if is_vertical_mirror_line(i,matrix):
      return i
  return -1

def get_mirror_number(matrix):
  ml = find_horizontal_mirror_line(matrix)
  if ml >= 0:
    return 100*(ml+1)
  ml = find_vertical_mirror_line(matrix)
  if ml >= 0:
    return ml+1
  return -1
    
data = load_data('input.dat')

print( sum( [get_mirror_number(matrix) for matrix in data] ) )
  