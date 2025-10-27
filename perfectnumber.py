#dividing_number = begining_number

#dividing_number = 6# is it perfect?

def findFactor(dividing_number):
    dividor = 1
    answer = 0
    list_of_factors = []
    while dividor >= 1 and dividor < dividing_number:
        answer = dividing_number % dividor
        if answer == 0:
            list_of_factors.append(dividor)
        dividor = dividor + 1
    #print(list_of_factors)
    return(list_of_factors)




def findPerfectNumber(begining_number, end_number):
    dividing_number = begining_number
    #list_of_answers = []
    while dividing_number < end_number:
        factor_list = findFactor(dividing_number)
        if sum(factor_list) == dividing_number:
            #list_of_answers.append(dividing_number)
            print(dividing_number)
        dividing_number = dividing_number + 1
    #return list_of_answers
    





print("where do you want the search for ")
begining_number = int(input("perfect numbers to start from (as a number)"))
    
print("where do you want the search for ")
end_number = int(input("perfect numbers to end at (as a number)"))



#last_list = findPerfectNumber(begining_number, end_number)
#print (last_list)
findPerfectNumber(begining_number, end_number)