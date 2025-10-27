from pylab import imshow,show,gray
from numpy import zeros,linspace

z = 0 + 0j
n=100

M = zeros([n,n],int)
xvalues = linspace(-2,2,n)
yvalues = linspace(-2,2,n)

for x in xvalues:
    for y in yvalues:
        c = complex(x,y)
        for i in range(100):
            z = z*z + c
            if abs(z) > 2.0:
                M[y,x] = 1
                break

imshow(M,origin="lower")
gray()
show()