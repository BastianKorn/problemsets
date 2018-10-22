from cs50 import get_int

def main():

    while True:
        height = get_int("number in range of 1 to 8: ")
        if height > 0 and height < 9:
            break

    for a in range(height):
        for l in range(height-a):
            print(" ", end="")

        for d in range(height-a, height + 1):
            print("#", end="")

        print(" ", end="")

        for k in range(height-a, height + 1):
            print("#", end="")

        print("")

if __name__ == "__main__":
    main()