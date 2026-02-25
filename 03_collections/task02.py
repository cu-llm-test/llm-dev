import collections

s = []
while True:
    i = input("")
    if i == "":
        break
    s.append(str(i))

s_join = ''.join(s)
col = collections.Counter(s_join)

for c in range(ord('a'), ord('z') + 1):
    if (col[chr(c)] > 0):
        print(f"{chr(c)}が{col[chr(c)]}個あります")
