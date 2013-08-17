def my_add(x, y):
    return x + y

def my_neg(x):
    return -x

def my_equal(x, y):
    return x == y

i = 0
n = input()
t = 0
while not my_equal(i, n):
    t = my_add(t, i)
    t = my_add(my_neg(i), t)
    i = my_add(i, 1)
print t
