// Restores JPEG files from memory card
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

const int SIZE = 512;

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "rb");

    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t buffer[SIZE];
    FILE *img = NULL;
    char filename[8];

    int i = 0;
    int flag = 0;

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, SIZE, card) == SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (flag == 1)
            {
                fclose(img);
            }

            flag = 1;

            sprintf(filename, "%03i.jpg", i);
            img = fopen(filename, "wb");

            fwrite(buffer, 1, SIZE, img);
            i++;
        }
        else if (flag == 1)
        {
            fwrite(buffer, 1, SIZE, img);
        }
    }

    // Close the last image file
    if (img != NULL)
    {
        fclose(img);
    }

    fclose(card);

    return 0;
}
