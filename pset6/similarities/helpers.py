from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    lines_a = set(a.splitlines()) #Splits Data in lines
    lines_b = set(b.splitlines()) #Splits Data in lines
    return lines_a & lines_b

def sentences(a, b):
    """Return sentences in both a and b"""

    sentences_a = set(sent_tokenize(a)) #Splits Data in sentences(sent)
    sentences_b = set(sent_tokenize(b)) #Splits Data in sentences(sent)
    return sentences_a & sentences_b

def substr(str, n):
    sublist = []
    for i in range(len(str)-n):
        sublist.append(str[i:i+n]) #Updates the list
    return sublist

def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    substrings_a = set(substr(a,n))
    substrings_b = set(substr(b,n))
    return substrings_a & substrings_b
