from nltk.tokenize import sent_tokenize
import sys

def lines(a, b):
    """Return lines in both a and b"""

    a = set(a.split("\n"))
    b = set(b.split("\n"))

    iden_lines = []

    [iden_lines.append(line) for line in a if line in b]

    return iden_lines


def sentences(a, b):
    """Return sentences in both a and b"""

    a = set(sent_tokenize(a, language='english'))
    b = set(sent_tokenize(b, language='english'))

    iden_sent = []

    [iden_sent.append(sent) for sent in a if sent in b]

    return iden_sent


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    def substr(x, n):
        x = set(x.split())
        x_substr = []
        for word in x:
            for j in range(len(word)):
                if len(word) < j + n:
                    continue
                else:
                    x_substr.append(word[j:j+n])
        return (list(set(x_substr)))

    a = substr(a, n)
    b = substr(b, n)

    iden_substr = []

    [ iden_substr.append(substr) for substr in a if substr in b]

    return iden_substr

