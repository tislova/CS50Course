#include <stdio.h>

int getSum(long number);
int getLastDigit(int final_sum);
void getValidation(int digit_count, long first_digits, int last_digit);

int main(void)
{
    long number;
    printf("Number: ");
    scanf("%ld", &number);

    int final_sum = getSum(number);
    int last_digit = getLastDigit(final_sum);

    int digit_count = 0;
    long first_digits = 0;
    long temp = number;

    while (temp > 0)
    {
        if (temp > 10 && temp < 100)
        {
            first_digits = temp;
        }
        temp = temp / 10;
        digit_count++;
    }

    getValidation(digit_count, first_digits, last_digit);

    return 0;
}

int getSum(long number)
{
    int odd_sum = 0, even_sum = 0;

    for (int i = 0; number > 0; i++)
    {
        int remainder_odd = number % 10;
        number = number / 10;
        int remainder_even = number % 10;
        number = number / 10;

        odd_sum += remainder_odd;

        remainder_even *= 2;

        if (remainder_even >= 10)
        {
            int even_last_digit = remainder_even % 10;
            remainder_even = remainder_even / 10;
            even_sum += even_last_digit + remainder_even;
        }
        else
        {
            even_sum += remainder_even;
        }
    }

    int sum = odd_sum + even_sum;
    return sum;
}

int getLastDigit(int final_sum)
{
    int last_digit;

    if (final_sum > 10)
    {
        last_digit = final_sum % 10;
    }
    else
    {
        last_digit = final_sum;
    }

    return last_digit;
}

void getValidation(int digit_count, long first_digits, int last_digit)
{
    if (last_digit != 0)
    {
        printf("INVALID\n");
    }
    else if (digit_count == 16 || digit_count == 15 || digit_count == 13)
    {
        if (first_digits == 37)
        {
            printf("AMEX\n");
        }
        else if (first_digits >= 51 && first_digits <= 55)
        {
            printf("MASTERCARD\n");
        }
        else if ((first_digits / 10) == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
