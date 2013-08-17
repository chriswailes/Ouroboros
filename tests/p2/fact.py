def fact(x):
    return 1 if x == 1 else x * fact(x - 1)

print fact(5)
