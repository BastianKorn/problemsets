#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

 int main(int argc, string argv[])
 {
    int keylength = strlen(argv[1]);
    string keyword = argv[1];

    if (argc != 2)
    {
        printf("Usage: ./vigenere key\n");
        return 1;
    }

    for (int i = 0; i < keylength; i++)
    {
        if (isalpha(keyword[i]) == 0)
        {
            printf("Alphabetical keys only!\n");
            return 1;
        }
    }

    string plaintext = get_string("Plaintext: ");
    int j = 0;

    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        j = j % keylength;

        if (isalpha(plaintext[i]))
        {
            if (islower(plaintext[i]) && islower(keyword[j]))
            {
                printf("%c", (((plaintext[i] - 97) + (keyword[j] - 97)) % 26) + 97);
            } else if (isupper(plaintext[i]) && islower(keyword[j]))
            {
                printf("%c", (((plaintext[i] - 65) + (keyword[j] - 97)) % 26) + 65);
            } else if (islower(plaintext[i]) && isupper(keyword[j]))
            {
                printf("%c", (((plaintext[i] - 97) + (keyword[j] - 65)) % 26) + 97);
            } else if (isupper(plaintext[i]) && isupper(keyword[j]))
            {
                printf("%c", (((plaintext[i] - 65) + (keyword[j] - 65)) % 26) + 65);
            }
            j++;
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
 }
