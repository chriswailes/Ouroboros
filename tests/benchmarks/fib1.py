def fib(n):
	m = 1
	
	while n:
		m = m * n
		n = n - 1
	
	return m

print(fib(3))

#i = 1000000
#while i:
#	fib(15)
#	
#	i = i - 1
