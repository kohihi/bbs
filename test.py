l1 = [i for i in range(10)]
l1 = l1*2
print(l1)
l2 = l1.copy()
print(l2)
d = {}.fromkeys(l2).keys()
print(type(d))