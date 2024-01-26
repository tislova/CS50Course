#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LENGTH 1000

void getCipher(char *text, const char *myString, char *encrypted_text);

int main(int argc, char *argv[])
{
    int i = 0;
    int len;

    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    for (i = 0, len = strlen(argv[1]); i < len; i++)
    {
        char first_character = toupper(argv[1][i]);

        for (int j = i + 1; j < len; j++)
        {
            if (first_character == toupper(argv[1][j]))
            {
                printf("Do not use repeated characters.\n");
                return 1;
            }
        }

        if (isalpha(argv[1][i]))
        {
            continue;
        }
        else
        {
            printf("Do not use special characters and numbers.\n");
            return 1;
        }
    }

    if (i != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    char text[LENGTH];
    printf("plaintext: ");
    fgets(text, sizeof(text), stdin);

    char encrypted_text[LENGTH];
    getCipher(text, argv[1], encrypted_text);

    printf("ciphertext: %s\n", encrypted_text);

    return 0;
}

void getCipher(char *text, const char *myString, char *encrypted_text)
{
    int i = 0;
    int len = strlen(text);

    for (i = 0; i < len; i++)
    {
        if (islower(text[i]))
        {
            encrypted_text[i] = tolower(myString[text[i] - 'a']);
        }
        else if (ispunct(text[i]) || isspace(text[i]) || isdigit(text[i]))
        {
            encrypted_text[i] = text[i];
        }
        else
        {
            encrypted_text[i] = toupper(myString[text[i] - 'A']);
        }
    }

    encrypted_text[i] = '\0';
}
