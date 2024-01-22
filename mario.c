#include <stdio.h>

void getHeight(int *height);
void spaces(int length);
void pyramide(int length);

int main(void)
{
    int height;
    getHeight(&height);

    int height1 = height;
    
    for (int l = 0; l < height; l++)
    {
        spaces(height1 - 1);
        pyramide(l);
        printf("\n");
        height1--;
    }

    return 0;
}

void getHeight(int *height)
{
    do
    {
        printf("Height: ");
        scanf("%i", height);
    }
    while (*height < 1 || *height > 8);
}

void spaces(int length)
{
    for (int i = 0; i < length; i++)
    {
        printf(" ");
    }
}

void pyramide(int length)
{
    for (int j = 0; j < length + 1; j++)
    {
        printf("#");
    }
    printf("  ");
    for (int k = 0; k < length + 1; k++)
    {
        printf("#");
    }
}