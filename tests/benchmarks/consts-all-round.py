i = 0
n = input()
t = 0
five = 5
ten = five
forty_two = five + 32 + ten + t
while i != n:
    t = forty_two + t + i + forty_two
    t = -i + t + forty_two + forty_two
    i = i + 1
print t
