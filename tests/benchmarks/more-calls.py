def f(a):
    return -a

_cnt = 1000000
x = 0
while _cnt:
    _cnt = _cnt + -1  
    x = f(f(f(f(f(f(6))))))

print x
