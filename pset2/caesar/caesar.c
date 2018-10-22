#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{

    if (argc == 2)
    {
        int inputKey = atoi(argv[1]);
        if(inputKey!=0)
        {
            string plaintext = get_string("plaintext: ");

            printf("ciphertext: ");
            for(int i=0;i<strlen(plaintext);i++)
            {
                if((plaintext[i] >= 'a' && plaintext[i] <= 'z') || (plaintext[i] >= 'A' && plaintext[i] <= 'Z') )
                {
                    if(isupper(plaintext[i]))
                    {
                        int c = (plaintext[i] - 65 + inputKey) % 26;
                        printf("%c", (c+65));
                    }else if(islower(plaintext[i]))
                        {
                        int c = (plaintext[i] - 97 + inputKey) % 26;
                        printf("%c", (c+97));
                        }
                }else
                    return 1;
            }
            printf("\n");
        }else
            printf("Usage: ./caesar key\n");
            return 2;
    }else
        printf("Usage: ./caesar key\n");
        return 3;
}
