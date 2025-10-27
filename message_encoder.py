import random 
listofletters = [" ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
alphebet = [" ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]



def randomNumbers(begining_seed, listofletters):
    scrambledletters = []
    amountoftries = 52
    random.seed(begining_seed)
    for i in range(53):
        #random.seed(begining_seed)
        random_number = (random.randint(0, amountoftries))
        letter = (listofletters[random_number])
        listofletters.remove(letter)
        scrambledletters.append(letter)
        amountoftries = amountoftries - 1
    return scrambledletters



def indexFinder (message, alphebet, i):
    #find the letter in the message
    letter = message[i]
    #find the index of the letter in the alphebet
    index = alphebet.index(letter)
    return index




begining_seed = input("what beginning seed do you want?")




message = input("what message do you want to encode?")

scrambledletters = randomNumbers(begining_seed, listofletters)
outputlist = []

i = 0
while i in range (len(message)):
    findwhere = indexFinder (message, alphebet, i)
    outputletter = (scrambledletters[findwhere])
    outputlist.append(outputletter)
    i = i + 1




joinything = ""
print(joinything.join(outputlist))
    
        
    






