def ff(x, y):
    return fg(x,y) + fg(x,y)

def fg(x, y):
    return fh(x,y) + fh(x,y)

def fh(x, y):
    return fi(x,y) + fi(x,y)

def fi(x, y):
    return fj(x,y) + fj(x,y)

def fj(x, y):
    return fk(x,y) + fk(x,y)

def fk(x, y):
    return fl(x,y) + fl(x,y)

def fl(x, y):
    return fm(x,y) + fm(x,y)

def fm(x, y):
    return fn(x,y) + fn(x,y)

def fn(x, y):
    return fo(x,y) + fo(x,y)

def fo(x, y):
    return fp(x,y) + fp(x,y)

def fp(x, y):
    return x + y

i = 0
n = input()
t = 0
while i != n:
    t = t + fm(1,2)
    t = t + -fm(1,2)
    i = i + 1
print t

