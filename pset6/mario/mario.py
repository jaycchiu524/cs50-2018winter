#Get input from user between 1 to 8
while True:
    number = input("Height: ")
    if number.isdigit():
        n = int(number)
        if n > 0 and n < 9:
            break

#Iterating n rows
for i in range (n):
    #print the space of the first half
    for j in range (n-i-1):
        print(" ", end="")

    #print the first half
    for k in range (n-i-1, n):
        print("#", end="")

    #print the space in-between
    print("  ", end="")

    #print the rest
    for l in range (n-i-1, n):
        print("#", end="")

    #to the next row
    print("")