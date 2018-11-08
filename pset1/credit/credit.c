#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main (void)
{
    long number = get_long("number: ");
    int length = 0;
    long buffer1 = number;
    long buffer2 = 0;
    long buffer3 = 0;
    long add = 0;
    long check = 0;

    do{
        buffer1 /= 10;
        length++;
    }while(buffer1 > 0);

    buffer1 = number;

    for(int i = 0; i < length; i++){
        buffer1 /= 10;
        buffer2 = buffer1 % 10;
        buffer2 *= 2;
        if (buffer2 > 9)
        {
            buffer3 = buffer2 % 10;
            buffer2 = buffer3 + (buffer2/10);
        }
        add += buffer2;
        buffer1 /= 10;
    }

    buffer1 = number;

    for(int i = 0; i < length; i++){
        buffer2 = buffer1 % 10;
        buffer1 /= 100;
        add += buffer2;
    }

    check = number / pow(10,length-1);

    switch(check)
    {
        case 4:
            if(length == 13 || length == 16){
                printf("VISA\n");
            }
            break;

    }

    check = number / pow(10,length-2);

    switch(check)
    {
        case 34:
            if (length == 15){
                printf("American Express\n");
            }
            break;

        case 37:
            if (length == 15){
                printf("American Express\n");
            }
            break;

         case 51:
            if (length == 16){
                printf("MasterCard\n");
            }
            break;

        case 52:
            if (length == 16){
                printf("MasterCard\n");
            }
            break;

        case 53:
            if (length == 16){
                printf("MasterCard\n");
            }
            break;

        case 54:
            if (length == 16){
                printf("MasterCard\n");
            }
            break;

         case 55:
            if (length == 16){
                printf("MasterCard\n");
            }
            break;
    }

    if (add % 10 == 0){
        printf("Valid\n");
    }else
        printf("Invalid\n");

    return 0;
}
