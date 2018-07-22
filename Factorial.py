def func_name(name=""):
    result = ""
    result = "Hello RC18, This is %s"%name
    return result

def facto(num=0):
    factorial = 1
    result = ""
    num = int(num)
    # check if the number is negative, positive or zero
    if num < 0:
        result = "Sorry, factorial does not exist for negative numbers"
    elif num == 0:
        result = "The factorial of 0 is 1"
    else:
        for i in range(1,num + 1):
            factorial = factorial*i
        result = factorial
    return result
