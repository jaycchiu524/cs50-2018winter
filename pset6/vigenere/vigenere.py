import sys

# Return error if argv != 2
if len(sys.argv) != 2 or not sys.argv[1].isalpha():
    sys.exit("Usage: python vigenere.py keyword")

# Assign var to argv[1] and get plaintext from user
keyword = sys.argv[1]
plaintext = input("plaintext: ")

# Convert keywords to ASCII number
key = [ord(x.lower())-ord("a") for x in list(sys.argv[1])]

# Set j as the key to recur the len(key)
j = 0

# Create a list
cipher = []
for i in range(len(plaintext)):
    # Case-sensitive, add converted ASCII number to corresponding letter
    # ord(plaintext[i]), add the key to it, chr() back to character
    if plaintext[i].islower():
        cipher.append(chr((((ord(plaintext[i])+key[j])-ord("a")) % 26)+ord("a")))
        j = j + 1
    elif plaintext[i].isupper():
        cipher.append(chr((((ord(plaintext[i])+key[j])-ord("A")) % 26)+ord("A")))
        j = j + 1

    # if not alpha, print directly
    else:
        cipher.append(plaintext[i])

    # Chagne j to 0 when key is about to end
    if j == len(sys.argv[1]):
        j = 0

# Join the list to string
ciphertext = "".join(cipher)

# Print out
print(f"ciphertext: {ciphertext}")