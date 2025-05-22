"""#multiplication of given two numbers

number1=20
number2=30
mul=number1*number2
print(mul)


#addition of given two numbers

number1=20
number2=30
add=number1+number2
print(add)


#multiplication of given two numbers

number1=40
number2=30
mul=number1*number2
print(mul)


#addition of given two numbers

number1=40
number2=30
add=number1+number2
print(add)


#using functions

def multiplication(number1,number2):
    mul=number1*number2
    return mul
def addition(number1,number2):
    add=number1+number2
    return add
'''print(multiplication(20,30))
print(addition(20,30))'''
print(multiplication(40,30))
print(addition(40,30))


#return their product only if the product is equal to or lower than 1000. Otherwise, return their sum.

number1=20
number2=30
mul=number1*number2
if mul<=1000:
    print(mul)
else:
    print(number1+number2)


#return their product only if the product is equal to or lower than 1000. Otherwise, return their sum.

number1=40
number2=30
mul=number1*number2
if mul<=1000:
    print(mul)
else:
    print(number1+number2)


#using functons

def multiplication(number1,number2):
    mul=number1*number2
    return mul
def addition(number1,number2):
    add=number1+number2
    return add
if multiplication(20,30)<=1000:
    print(multiplication(20,30))
else:
    print(addition(20,30))

def multiplication(number1,number2):
    mul=number1*number2
    return mul
def addition(number1,number2):
    add=number1+number2
    return add
if multiplication(40,30)<=1000:
    print(multiplication(40,30))
else:
    print(addition(40,30))

#code to iterate the first 10 numbers, and in each iteration, print the sum of the current and previous number.
for i in range(10):
    if i==0:
        print("current number:",i,"sum of the current num and previous num is:",i)
    else:
         print("current number:",i,"sum of the current num and previous num is:",i+i-1)


#code to accept a string from the user and display characters present at an even index number.

name=input("Enter your string:")
size=len(name)
for i in range(0,size,2):
    print("characters present at even index number are:",name[i])
"""

  

