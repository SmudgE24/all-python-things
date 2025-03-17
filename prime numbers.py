import time
#import math
#import pandas
#from typing import List
   
#this function allows the user to return the number of factors a number has
def isPrimeNumber(n1):
    n2 = 1
    count = 0
    while n2 <= n1:
        if n1 % n2 == 0:
            count = count + 1
        n2 = n2 + 1
    return count
    
    
n1 = 0
prime_no_list = [] # type: List[int]
target = 1000000



while n1 <= target:#this ends the program when a spicific number is reached
#while n1 <= n1:#this keeps going for ever
    count = isPrimeNumber(n1)
    if count == 2:
        #prime_no_list.append(n1)
        print (n1)
        #time.sleep(0.1)
    n1 = n1 + 1

#print (prime_no_list)
