from cs50 import get_string
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python bleep.py dictionary")

    # Open .txt file and input all words into set()
    words = set()
    dictionary = sys.argv[1]
    with open(dictionary, "r") as infile:
        for line in infile:
            words.add(line.strip("\n"))

    text = (input("What message would you like to censor?\n")).split()

    # Create a list to store censored words
    censored = []

    # Change the characters to "*" if the words are in set()
    for word in text:
        # tolower all words to be non case-sensitive
        if (word.lower()) in words:
            s = list(word)
            for i in range(len(word)):
                s[i] = "*"
            # Combine characters to a word
            s = "".join(s)
            censored.append(s)

        # if not, just append directly
        else:
            censored.append(word)

    # Combined all words to a string
    censored = " ".join(censored)

    print(censored)


if __name__ == "__main__":
    main()
