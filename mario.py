# Prints out a pyramid of asterisks
def spaces(length1):
    for i in range(length1 - 1):
        print(" ", end='')


def pyramide(length):
    for i in range(length):
        print("#", end='')
    print("  ", end='')

    for i in range(length):
        print("#", end='')
    print("\n", end='')


def main():
    height = 0

    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                break
        except ValueError:
            print("Type an integer between 1 and 8")
    height1 = height
    for i in range(height):
        spaces(height1)
        pyramide(i + 1)
        height1 -= 1


main()
