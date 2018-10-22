from cs50 import get_int

def main():

    number = get_int("Nummer: ")
    length = len(str(number))
    buffer1 = number
    addnumber = 0

    for i in range(length):
        buffer1 = buffer1 // 10
        buffer2 = buffer1 % 10
        buffer2 = buffer2 * 2
        if buffer2 > 9:
            buffer3 = buffer2 % 10
            buffer2 = buffer3 + (buffer2//10)
        addnumber = addnumber + buffer2
        buffer1 = buffer1 // 10

    buffer1 = number

    for i in range(length):
        buffer2 = buffer1 % 10
        buffer1 = buffer1 // 100
        addnumber = addnumber + buffer2

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