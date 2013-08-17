def derivative(f):
    epsilon = 1
    return lambda x: (f((10 * x) + epsilon) - f(10 * x)) / (10 * epsilon)

def square(x):
    return x * x

ds = derivative(square)

print ds(10)
