# This is a guess the number game.
import random
#guess rendom number
#def guess_high_or_low(mynum):
#    result = "wrong num"
#    if(mynum <= 0):
#        return 
#    n = random.randint(1, 20)
#    guess = mynum
#    if guess < n:
#        result = "guess is low"
#    elif guess > n:
#        result = "guess is high"
#    else:
#        result = "you guessed it!"
#    return result

#convert Celsius to Fahrenheit
def celsius_to_fahrenheit(mycelsius=0):
    celsius = float(mycelsius)
    # calculate temperature in Fahrenheit
    fahrenheit = (celsius * 1.8) + 32
    return fahrenheit

#convert kilometers to miles
def kilometers_to_miles(mykm=0):
    km = float(mykm)
    # conversion factor
    conv_fac = 0.621371
    # calculate miles
    miles = km * conv_fac
    return miles

