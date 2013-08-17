def map(f, l, i, n):
	return [f(l[i])] + map(f, l, i + 1, n) if i != n else []

print map(lambda x: x + 1, [0, 1], 0, 2)
