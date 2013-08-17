def map(l, i, n):
	return [l[i] + 1] + map(l, i + 1, n) if i != n else []

print map([0, 1], 0, 2)
