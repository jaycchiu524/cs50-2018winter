from cs50 import get_string

# Get credit number from user
while True:
    number = get_string("Number: ")
    if number.isdigit():
        break

# American Express uses 15-digit numbers
# MasterCard uses 16-digit numbers
# Visa uses 13- and 16-digit numbers.
if (len(number) == 13 or len(number) == 15 or len(number) == 16):

    if len(number) % 2 == 0:
        # Luhn’s Algorithm, extract every other digit from the second-last positions.
        check_1 = number[::2]

        # Luhn’s Algorithm, extract every other digit from last positions.
        check_2 = number[1::2]

    else:
        # Vice versa
        check_1 = number[1::2]
        check_2 = number[::2]

    # Multiply by 2
    check_1_m2 = [int(x)*2 for x in str(check_1)]
    # Sum up all digits
    check_1_str = "".join(str(x) for x in check_1_m2)

    # Sum up all digits of the rest number
    check_2_str = "".join(str(x) for x in check_2)

    # Add two sums together
    check_sum_1 = sum(int(x) for x in check_1_str)
    check_sum_2 = sum(int(x) for x in check_2_str)
    check_sum = check_sum_1 + check_sum_2

    # All American Express numbers start with 34 or 37
    # MasterCard numbers start with 51, 52, 53, 54, or 55
    # Visa numbers start with 4.
    if (check_sum % 10) == 0:
        if len(number) == 15 and number[0] == '3' and (number[1] in ['4', '7']):
            print("AMEX")
        elif len(number) == 16 and number[0] == '5' and (number[1] in ['1', '2', '3', '4', '5']):
            print("MASTERCARD")
        elif (len(number) == 13 or 16) and number[0] == '4':
            print("VISA")
        else:
            print("INVALID")

else:
    print("INVALID")

