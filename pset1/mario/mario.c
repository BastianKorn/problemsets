#include <cs50.h>
#include <stdio.h>

int main (void)
{
    int height;
    int c = 0;

    while(height < 1 || height > 8) {
        printf("Welche Hoehe?\n");
        height = get_int();
    }

    for(int i = height; i > 0; i--) { // Höhe
        for(int space = 0; space < i - 1; space++) { //Leerzeichen vor #
            printf(" ");
        }

        printf("#"); //Gibt ein # aus
        c++;

        for (int hash = 0; hash < c - 1; hash++) { //Gibt zusätzliche # aus
            printf("#");
        }

        printf(" "); // Leerzeichen

        for (int hash = 0; hash < c; hash++) { //Gibt zusätzliche # aus
            printf("#");
        }
        printf("\n");
    }
}
