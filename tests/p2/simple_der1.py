def less_helper(x, y, xp, yp):
    return True if xp == y else (False if yp == x else less_helper(x, y, xp + 1, yp + 1))

def less(x, y):
    return less_helper(x, y, x + 1, y)

print less(1, 0)
 
