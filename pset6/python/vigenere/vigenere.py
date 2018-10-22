import sys
from cs50 import get_string

def main():

    if len(sys.argv) is not 2:
        print("Usage: python caesar.py key")
        return 1

    keyword = sys.argv[1]
    keylength = len(keyword)
    j = 0

    if str.isalpha(keyword) is False:
        print("Alphabetical keys only!")
        return 2

    print("This is the name of the script: ", sys.argv[0])
    print("This is the key: ", keyword)
    print("This is the keylength: ", keylength)
    print("Number of arguments: ", len(sys.argv))
    print("The arguments are: " , str(sys.argv))
    plaintext = get_string("plaintext: ")

    print("ciphertext: ", end="")

    for i in range(len(plaintext)):

        j = j % keylength

        if str.isalpha(plaintext[i]) is True:

            if str.islower(plaintext[i]) is True and str.islower(keyword[j]) is True:
                erg = ((ord(plaintext[i]) - 97) + (ord(keyword[j]) - 97) % 26) + 97
                print(chr(erg), end="")

            elif str.isupper(plaintext[i]) is True and str.islower(keyword[j]) is True:
                erg = ((ord(plaintext[i]) - 65) + (ord(keyword[j]) - 97) % 26) + 65
                print(chr(erg), end="")

            elif str.islower(plaintext[i]) is True and str.isupper(keyword[j]) is True:
                erg = ((ord(plaintext[i]) - 97) + (ord(keyword[j]) - 65) % 26) + 97
                print(chr(erg), end="")

            elif str.isupper(plaintext[i]) is True and str.isupper(keyword[j]) is True:
                erg = ((ord(plaintext[i]) - 65) + (ord(keyword[j]) - 65) % 26) + 65
                print(chr(erg), end="")
        j = j+1

    print()

if __name__ == "__main__":
    main()