def ff(x, y):
    if x == 1:
        return fg(x,y)
    else:
        return fg(x,y) + fg(x,y)

def fg(x, y):
    if x == 1:
        return fh(x,y)
    else:
        return fh(x,y) + fh(x,y)

def fh(x, y):
    if x == 1:
        return fi(x,y)
    else:
        return fi(x,y) + fi(x,y)

def fi(x, y):
    if x == 1:
        return fj(x,y)
    else:
        return fj(x,y) + fj(x,y)

def fj(x, y):
    if x == 1:
        return fk(x,y)
    else:
        return fk(x,y) + fk(x,y)

def fk(x, y):
    if x == 1:
        return fl(x,y)
    else:
        return fl(x,y) + fl(x,y)

def fl(x, y):
    if x == 1:
        return fm(x,y)
    else:
        return fm(x,y) + fm(x,y)

def fm(x, y):
    if x == 1:
        return fn(x,y)
    else:
        return fn(x,y) + fn(x,y)

def fn(x, y):
    if x == 1:
        return fo(x,y)
    else:
        return fo(x,y) + fo(x,y)

def fo(x, y):
    if x == 1:
        return fp(x,y)
    else:
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

