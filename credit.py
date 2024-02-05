#Determines the validity and type of credit card
def main():
    number = int(input("Number: "))
    final_sum = getSum(number)
    last_digit = getLastDigit(final_sum)

    temp = number
    digit_count = len(str(number))

    while temp > 0:
        if 10 < temp < 100:
            first_digits = temp
        temp = temp // 10

    getValidation(digit_count, first_digits, last_digit)


def getSum(number):
    odd_sum = 0
    even_sum = 0

    i = 0
    while number > 0:
        remainder_odd = number % 10
        number = number // 10
        remainder_even = number % 10
        number = number // 10

        odd_sum += remainder_odd

        remainder_even *= 2

        if remainder_even >= 10:
            even_last_digit = remainder_even % 10
            remainder_even = remainder_even // 10
            even_sum += even_last_digit + remainder_even
        else:
            even_sum += remainder_even

        i += 1

    sum = odd_sum + even_sum
    return sum


def getLastDigit(final_sum):
    if final_sum > 10:
        last_digit = final_sum % 10
    else:
        last_digit = final_sum

    return last_digit


def getValidation(digit_count, first_digits, last_digit):
    if last_digit != 0:
        print("INVALID")
    elif digit_count == 16 or digit_count == 15 or digit_count == 13:
        if first_digits == 37:
            print("AMEX")
        elif first_digits >= 51 and first_digits <= 55:
            print("MASTERCARD")
        elif (first_digits // 10) == 4:
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")


main()
