import sys

a = "Harvard CS50 1234 Harvard"
b = "Harlo CS55 12234"
n = 3

def substr(x, n):
    x = set(x.split())
    x_substr = []
    for word in x:
        for j in range(len(word)):
            if len(word) < j + n:
                continue
            else:
                x_substr.append(word[j:j+n])
    return (x_substr)

a = substr(a, n)
b = substr(b, n)

iden_substr = []

[ iden_substr.append(substr) for substr in a if substr in b]

print (iden_substr)