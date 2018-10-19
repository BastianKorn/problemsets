#include <stdio.h>
#include <stdlib.h>
#include "bmp.h"
#include <cs50.h>

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        fprintf(stderr, "Usage: ./recover input\n");
        return 1;
    }

    FILE *card_ptr = fopen("card.raw", "r");

    if(card_ptr == NULL)
    {
        fprintf(stderr, "File not found");
        return 2;
    }

    BYTE buffer[512];
    bool found = false;
    FILE *new_jpg_ptr;
    int file_counter = 0;

    while(fread(buffer, 1, 512, card_ptr) != 0x00)
    {
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if(!found)
            {
                found = true;

                char filename[8];
                sprintf(filename, "%03i.jpg", file_counter++);
                new_jpg_ptr = fopen(filename, "w");
                if(new_jpg_ptr == NULL)
                {
                    return 3;
                }
                fwrite(buffer,1,512 ,new_jpg_ptr);

            }else
            {
                fclose(new_jpg_ptr);
                char filename[8];
                sprintf(filename, "%03i.jpg", file_counter++);
                new_jpg_ptr = fopen(filename, "w");
                if(new_jpg_ptr == NULL)
                {
                    return 3;
                }
                fwrite(buffer,1,512 ,new_jpg_ptr);
            }
        }else
        {
            if(found)
            {
                fwrite(buffer,1,512 ,new_jpg_ptr);
            }
        }

    }

    fclose(new_jpg_ptr);
    fclose(card_ptr);
return 0;
}