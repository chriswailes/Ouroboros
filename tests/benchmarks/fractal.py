def mult(x, y):
    return 0 if x == 0 else (y if x == 1 else y + mult(x + -1, y))

def less_helper(x, y, xp, yp):
    return True if xp == y else (False if yp == x else less_helper(x, y, xp + 1, yp + 1))

def less(x, y):
    return less_helper(x, y, x + 1, y)

def div(x, y):
    if less(y, x):
        return 0
    else:
        return 1 + div(x + -y, y)

BAILOUT = 16
MAX_ITERATIONS = 1000
    
class Iterator:
    def __init__(self):
        y = -39
        while y != 39:
            print 2
            x = -39
            while x != 39:
                i = self.mandelbrot(div(x,40), div(y,40))
                if i == 0:
                    print 1
                else:
                    print 0
                x = x + 1
            y = y + 1
    def mandelbrot(self, x, y):
        cr = div(mult(2,y) + -1, 2)
        ci = x
        zi = 0
        zr = 0
        i = 0
        while True:
            i = i + 1
            temp = mult(zr, zi)
            zr2 = mult(zr, zr)
            zi2 = mult(zi, zi)
            zr = zr2 + -zi2 + cr
            zi = temp + temp + ci
            if less(BAILOUT, zi2 + zr2):
                return i
            else:
                0
            if less(MAX_ITERATIONS, i):
                return 0
            else:
                0
Iterator()


