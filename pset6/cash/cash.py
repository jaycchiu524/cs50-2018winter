from cs50 import get_float

#Get input from user
while True:
    owed = get_float("Change owed: ")
    if owed > 0:
        break

#Round the number to 2 d.p.
cents = round(owed, 2) * 100

#Declare var for the number of each coin
quarters = dimes = nickles = pennies = 0

#Do the math
while cents >= 25:
    cents = cents - 25
    quarters = quarters + 1

while cents >= 10:
    cents = cents - 10
    dimes = dimes + 1

while cents >= 5:
    cents = cents - 5
    nickles = nickles + 1

pennies = int(cents)

#Sum up the number of coins
print(quarters+dimes+nickles+pennies)