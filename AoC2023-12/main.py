def load_data( file_name ):
  with open(file_name,'r') as file:
    data = [line.strip() for line in file]
  return arrange_data(data)

def arrange_data(data):
  arranged_data = []
  for shelf in data:
    spr_lst, cnd_recs = shelf.split()
    cnd_rec = [ int(x) for x in cnd_recs.split(',')]
    arranged_data.append( (spr_lst, cnd_rec) )
  return arranged_data

def count_arr(slist, clist):
  slist = slist.strip('.')
  if not clist:
    return 0 if '#' in slist else 1
  if len(slist) == 0 or sum(clist) > len(slist) - slist.count('.'):
    return 0
    
  match slist[0]:
    case '?':
      c1 = count_arr('.'+slist[1:],clist)
      c2 = count_arr('#'+slist[1:],clist)
      return c1 + c2
    case '.':
      return count_arr(slist[1:],clist)
    case '#':
      # The first clist[0] springs must be defects
      if '.' in slist[: clist[0]]:
        return 0
      # Are we at the end of the list?
      if len(slist) == clist[0]:
        return count_arr('', clist[1:])
      # Else check for separator
      elif slist[clist[0]] == '#':
        return 0
      # Separator is . or ?
      else:
        return count_arr(slist[clist[0]+1:], clist[1:])
  print('This should not happen!')
  return 0

def get_cache(s,c,cache):
  if s in cache and c in cache[s]:
    return cache[s][c]
  else:
    print('No cache for s: {}, c: {}'.format(s,c))
    return -1000

def arrangements(s_lst,i_s,c_lst,i_c,cache):
  s = s_lst[i_s:]
  c = c_lst[i_c:]
  # All records have been matched
  if not c:
    return 0 if '#' in s else 1
  # s must have room for all remaining records and separators
  if len(s) < sum(c) + len(c) - 1:
    return 0
  # Handle next spring and next record
  match s[0]:
    case '.':
      return cache[i_s+1][i_c]
    case '?':
      arr = 0
      arr += get_cache(i_s+1,i_c,cache)
      s_new = s_lst[0:i_s] + '#' + s_lst[i_s+1:]
      arr += arrangements(s_new,i_s,c_lst,i_c,cache)
      return arr
    case '#':
      # Check for functioning springs
      if '.' in s[:c[0]]:
        return 0
      # Are we at the end of the list?
      if len(s) == c[0]:
        return get_cache(len(s_lst),i_c+1,cache)
      # Separator must be . or ?
      elif s[c[0]] == '#':
        return 0
      # Separator is . or ?
      else:
        return cache[ i_s + c[0] + 1 ][ i_c + 1 ]  
  print('This should not happen!')
  return 0

def count_arr2( spr_lst, cnd_rec):
  cache = {}
  for i_s in range(len(spr_lst),-1,-1):
    cache[i_s] = {}
    for i_c in range(len(cnd_rec),-1,-1):
      cache[i_s][i_c] = arrangements(spr_lst,i_s,cnd_rec,i_c,cache)
  return cache[0][0]

data = load_data('input.dat')

arr_sum = 0
for spr_lst, cnd_rec in data:
  arr_sum += count_arr2(spr_lst, cnd_rec)
print('Part 1:', arr_sum)

arr_sum = 0
for spr_lst, cnd_rec in data:
  s = spr_lst + '?' + spr_lst + '?' + spr_lst + '?' + spr_lst + '?' + spr_lst 
  c = cnd_rec + cnd_rec + cnd_rec + cnd_rec + cnd_rec
  arr_sum += count_arr2(s, c)
print('Part 2:', arr_sum)