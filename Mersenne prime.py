import time as t

the_power = 1


def powerOfTwo(the_power):
    thepoweroftwo = pow(2, the_power)
    return thepoweroftwo
        

def isPrime(the_power):
    powerof = powerOfTwo(the_power)
    testnumber = powerof - 1
    n2 = 1
    count = 0
    while n2 <= testnumber:
        if testnumber % n2 == 0:
            count = count + 1
        n2 = n2 + 1
    if count == 2:
        return True
    else:
        return False
        
def isTrue(the_power):
    while the_power == the_power:
        True_or_False = isPrime(the_power)
        if True_or_False == True:
            print(pow(2, the_power) - 1, " is a Mersenne prime")
        #else:
            #print(pow(2, the_power) - 1, "is not a Mersenne prime")
        the_power = the_power + 1
        t.sleep(1)
        
        
        
        


isTrue(the_power)
