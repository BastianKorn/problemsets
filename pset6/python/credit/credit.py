from cs50 import get_int

def main():

    number = get_int("Nummer: ")

    length = len(str(number))

    cnumber = number
    addnumber = 0

    for i in range(length):
        cnumber = cnumber // 10
        ccnumber = cnumber % 10
        ccnumber = ccnumber * 2
        if ccnumber > 9:
            cccnumber = ccnumber % 10
            ccnumber = cccnumber + (ccnumber//10)
        addnumber = addnumber + ccnumber
        cnumber = cnumber // 10

    cnumber = number

    for i in range(length):
        ccnumber = cnumber % 10
        cnumber = cnumber // 100
        addnumber = addnumber + ccnumber

    check = number // pow(10,length-1)

    if check == 4:
        if length == 13 or length == 16:
            print("VISA")

    check = number // pow(10,length-2)

    if check == 34:
        if length == 15:
            print("American Express")
    elif check == 37:
        if length == 15:
            print("American Express")
    elif check == 51:
        if length == 16:
            print("MasterCard")
    elif check ==52:
        if length == 16:
            print("MasterCard")
    elif check == 53:
        if length == 16:
            print("MasterCard")
    elif check == 54:
        if length == 16:
            print("MasterCard")
    elif check == 55:
        if length == 16:
            print("MasterCard")


    if addnumber % 10 == 0:
        print("Valid")
    else:
        print("Invalid")

if __name__ == "__main__":
    main()