#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(char text[1000]);
int count_words(char text[1000]);
int count_sentences(char text[1000]);

int main(void)
{
    // Prompt the user for some text
    char text[1000];
    printf("Text: ");
    scanf("%999s", text);

    // Count the number of letters, words, and sentences in the text
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Compute the Coleman-Liau index
    double L = ((double) letters / words) * 100;
    double S = ((double) sentences / words) * 100;
    double index = 0.0588 * L - 0.296 * S - 15.8;
    float index1 = round(index);
    int index2 = (int)index1;

    // Print the grade level
    if (index2 < 16 && index2 >= 1)
    {
        printf("Grade %i\n", index2);
    }
    else if (index2 >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Before Grade 1\n");
    }
}

int count_letters(char text[1000])
{
    // Return the number of letters in text
    int j = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isalpha(text[i]))
        {
            j++;
        }
    }
    return j;
}

int count_words(char text[1000])
{
    // Return the number of words in text
    int j = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isspace(text[i]))
        {
            j++;
        }
    }
    return j + 1;
}

int count_sentences(char text[1000])
{
    // Return the number of sentences in text
    int j = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (ispunct(text[i]))
        {
            if (text[i] == '!' || text[i] == '.' || text[i] == '?')
            {
                j++;
            }
        }
    }
    return j;
}