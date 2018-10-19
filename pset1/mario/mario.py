from cs50 import get_int

def main():

    while True:
        h = get_int("number in range of 1 to 8: ")
        if h >= 0 and h <= 9:
            break

    for a in range(h):

        for l in range(h-a):
            print(" ", end="")

        for d in range(h-a, h + 1):
            print("#", end="")

        print(" ", end="")

        for k in range(h-a, h + 1):
            print("#", end="")

        print("")

if __name__ == "__main__":
    main()