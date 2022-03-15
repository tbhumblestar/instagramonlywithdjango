

n = int(input())
 
def countdown(n):
  n = n+1
  def count():
    nonlocal n
    n -= 1
    return n
  return count


c = countdown(n)
for i in range(n):
    print(c(), end=' ')
