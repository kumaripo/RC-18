#Python Program to Check if a Number is Positive, Negative or 0
def positive_or_negative_func(num = 0):
    type_of_num = ""
    num = int(num)
    if num > 0:
        type_of_num = "Positive number"
    elif num == 0:
        type_of_num = "Zero"
    else:
        type_of_num = "Negative number"
    return type_of_num


#Python Program to Check if a Number is Odd or Even
def odd_even_func(num = 0):
    type_of_num = ""
    num = int(num)
    if (num % 2) == 0:
        type_of_num = "Even"
    else:
        type_of_num = "Odd"
    return type_of_num

#Python Program to Check Prime Number
def prime_num(num = 0):
    num = int(num)
    type_of_num = ""
    if num > 1:
    # check for factors
        for i in range(2,num):
            if (num % i) == 0:
                type_of_num = "it is not a prime number"
                break
        else:
            type_of_num = "it is a prime number"
    # if input number is less than
    # or equal to 1, it is not prime
    else:
        type_of_nums = "it is not a prime number"
    return type_of_num
