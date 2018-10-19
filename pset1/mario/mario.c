#include <cs50.h>
#include <stdio.h>

int main (void)
{
    int h;
    int c = 0;
    do
    {
        printf("Welche Hoehe?\n");
        h = get_int();
    }while(hoch < 1 || hoch > 8);

    for(int a = h; a > 0; a--) //Höhe
    {

        for(int l = 0; l < a - 1; l++)  //Leerzeichen vor #
        {
            printf(" ");
        }

        printf("#"); //Gibt ein # aus
        c++;

        for (int d = 0; d < c - 1; d++) //Gibt zusätzliche # aus
        {
            printf("#");
        }

        printf(" "); // Leerzeichen

        for (int d = 0; d < c; d++) //Gibt zusätzliche # aus
        {
            printf("#");
        }

        printf("\n");
    }
}
