import sys
from cs50 import get_string

def main():

    if len(sys.argv) is not 2:
        print("Usage: python caesar.py key")
        return 1

    if sys.argv[1] is 0:
        print("Usage: python caesar.py key")
        return 2

    print("This is the name of the script: ", sys.argv[0])
    print("This is the keysize: ", sys.argv[1])
    print("Number of arguments: ", len(sys.argv))
    print("The arguments are: " , str(sys.argv))
    plaintext = get_string("plaintext: ")
    inputKey = sys.argv[1];

    for i in range(len(plaintext)):
        if (plaintext[i] >= 'a' and plaintext[i] <= 'z') or (plaintext[i] >= 'A' and plaintext[i] <= 'Z'):
            if str.isupper(plaintext[i]):
                c = (ord(plaintext[i]) - 65 + int(inputKey)) % 26
                print(chr(c+65), end="")
            elif str.islower(plaintext[i]):
                c = (ord(plaintext[i]) - 97 + int(inputKey)) % 26
                print(chr(c+97), end="")
        else:
            return 3

    print()



if __name__ == "__main__":
    main()