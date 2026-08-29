import copy
import sys
going = True
while going:
    length = int(input("How many equations would you like? "))
    if length > 20:
        print("More than 20 is too many")
    elif length < 2:
        print("Less than 2 is too few")
    else:
        going = False

strOfVars = "abcdefghijklmnopqrstuvwxyz"
listOfVars = []
for i in range(len(strOfVars)):
    listOfVars.append(strOfVars[i])
print("Please put a minus (if you want one) when this code asks you for a coefficient")

ListOfVariables = []
equals = []
for i in range(length):
    if (i + 1) == 1:
        extra = "st"
    elif (i + 1) == 2:
        extra = "nd"
    elif (i + 1) == 3:
        extra = "rd"
    else:
        extra = "th"
    a = (str(i + 1) + extra)
    firstEquationsListOfVariables = []
    for j in range(length):
        if (j + 1) == 1:
            extra2 = "st"
        elif (j + 1) == 2:
            extra2 = "nd"
        elif (j + 1) == 3:
            extra2 = "rd"
        else:
            extra2 = "th"
        b = (str(j + 1) + extra2)
        a_variable = int(input(f"What is your {a} equation's {b} variable's coefficient: "))
        firstEquationsListOfVariables.append(a_variable)
    ListOfVariables.append(firstEquationsListOfVariables)
    e = int(input("What does this equal? "))
    equals.append(e)
    body = ''
    for q in range(len(firstEquationsListOfVariables)):
        body = body + str(firstEquationsListOfVariables[q]) + str(listOfVars[q])
        if q + 1 != len(firstEquationsListOfVariables):
            body = body + "+"
    print("Your", a, "equation is:", body, "=", e)

origin1 = copy.deepcopy(ListOfVariables)
origin2 = copy.deepcopy(equals)

def solve(A, b, number1, number2, column):
    list1 = A[number1]
    list2 = A[number2]
    multL1 = list2[column]
    multL2 = list1[column]
    list3 = []
    for i in range(len(list1)):
        list3.append(list2[i] * multL2 - list1[i] * multL1)
    e1 = b[number1]
    e2 = b[number2]
    newE = e2 * multL2 - e1 * multL1
    return [list3, newE]




A = copy.deepcopy(ListOfVariables)
print(A)
b = copy.deepcopy(equals)
n = len(A)
results = []
for step in range(n - 1):
    m = len(A)
    for z in range(m):
        # skip if pivot invalid
        if z >= len(A[z]): 
            continue
        if A[z][z] == 0:
            continue
        for i in range(z + 1, m):
            if z >= len(A[i]):
                continue
            newRow, newE = solve(A, b, z, i, z)
            A[i] = newRow
            b[i] = newE
    print("\nAfter elimination:")
    for i in range(len(A)):
        print(A[i], "=", b[i])
    f = m - 1
    if A[f][f] == 0:
        print("Can not solve this simultanious equation   ):")
        sys.exit()
    val = b[f] / A[f][f]
    varname = listOfVars[f]
    print(f"{varname} = {val}")
    results.append(val)
    for i in range(m):
        coeff = A[i][f]
        b[i] = b[i] - coeff * val 
    for i in range(m):
        A[i].pop(f)
    A.pop(f)
    b.pop(f)

if len(A) == 1:
    final_val = b[0] / A[0][0]
    results.append(final_val)
    print(f"{listOfVars[0]} = {final_val}")
results.reverse()
print()
print("Results:")
for i, v in enumerate(results):
    print(f"{listOfVars[i]} = {v}")


for col in range(int(length)):
    for i in range(col + 1, int(length)):
        if ListOfVariables[col][col] == 0:
            continue
        list3, newE = solve(ListOfVariables, equals, col, i, col)
        ListOfVariables[i] = list3
        equals[i] = newE

print()
print("After elimination:")
for i in range(int(length)):
    print(ListOfVariables[i], "=", equals[i])
print(A)