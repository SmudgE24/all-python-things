a = 0
print (a)
b = 1
print (b)
c = (a + b)
print (c)

for i in range(10):
    a=b
    b=c
    c=(a+b)
    print (c)