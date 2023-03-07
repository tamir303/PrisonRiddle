# author: itzhik aviv
# https://www.youtube.com/watch?v=iSNsgj1OCLA&ab_channel=Veritasium
import sys
import random
def pr(l, printF):
    n = len(l)
    u = n * [0]
    for j in range(n):
      if printF:
          print ("j =", j)
      v = []
      while True:
        p = random.randint(0, n - 1)
        if p not in v:
           v.append(p)
           if p == j:
              break
      if len(v) <= (n // 2):
           u[j] = 1
      if printF:
         print("list l:", end=" ")
         for o in range(n):
             print(l[o], end=" ")
         print()
         print("list v:", end =" ")
         for g in range(len(v)):
             print (v[g], end = " ")
         print()
         if len(v) <= (n // 2):
             print("prisoner number ", j, " succeeded ",
                   "chain length = ", len(v))
         else:
             print("prisoner number ", j, " failed ",
                   "chain length =", len(v))
    if printF:
        print("number of prisoners that find their number is:",
              sum(u), "\n    from", n, " prisoners.\n")
    if sum(u) == n:
        return True
    else:
        return False

def main(n ,k, printF):
    if not isinstance(n, int):
        print("n =", n, " n must be integer.")
        return
    if n < 2:
        print("n =", n, " n must be > 1.")
        return
    if not isinstance(k, int):
        print("k =", k, " k must be integer.")
        return
    if k <= 0:
            print("k =", k, " k must be > 0.")
    s = 0
    for i in range(k):
        if printF:
            print ("round number", (i+1))
        l = n * [0]
        for j in range(n):
            l[j] = j
        random.shuffle(l)
        if printF:
          print ("iteration number =", i)
        if pr(l, printF):
            s += 1
    print("n =", n, " k =", k, " s = ", s,
          "\ns / k in % =", 100 * (s / k))

sys.stdout = open("PrisonersWitoutOptimizeReults.txt", "w")
main(100, 10000, False)
sys.stdout.close()
