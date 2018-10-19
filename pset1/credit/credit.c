#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main (void)
{
    long nummer = get_long("Nummer: ");
    int laenge = 0;
    long lnummer = 0;
    long cnummer = 0;
    long ccnummer = 0;
    long cccnummer = 0;
    long addnummer = 0;
    long check = 0;

    lnummer = nummer;
    do{
        lnummer = lnummer /10;
        laenge++;
    }while(lnummer > 0);

    cnummer = nummer;

    for(int i=0;i<laenge;i++)
    {
        cnummer /= 10;
        ccnummer = cnummer % 10;
        ccnummer = ccnummer * 2;
            if(ccnummer > 9)
            {
                cccnummer = ccnummer % 10;
                ccnummer = cccnummer + (ccnummer/10);
            }
        addnummer = addnummer + ccnummer;
        cnummer /= 10;
    };

    cnummer = nummer;

    for(int i=0;i<laenge;i++)
    {
        ccnummer = cnummer % 10;
        cnummer /= 100;
        addnummer = addnummer + ccnummer;
    }

   check = nummer / pow(10,laenge-1);
   switch(check)
    {
        case 4:
           if(laenge == 13 || laenge == 16)
           {
            printf("VISA\n");
           }
           break;
   }

    check = nummer / pow(10,laenge-2);

    switch(check)
    {
        case 34:
           if(laenge == 15)
           {
            printf("American Express\n");
           }
           break;

        case 37:
           if(laenge == 15)
           {
            printf("American Express\n");
           }
           break;

         case 51:
           if(laenge == 16)
           {
            printf("MasterCard\n");
           }
           break;

         case 52:
           if(laenge == 16)
           {
            printf("MasterCard\n");
           }
           break;

        case 53:
           if(laenge == 16)
           {
            printf("MasterCard\n");
           }
           break;

        case 54:
           if(laenge == 16)
           {
            printf("MasterCard\n");
           }
           break;

         case 55:
           if(laenge == 16)
           {
            printf("MasterCard\n");
           }
           break;
    }

    if(addnummer%10 == 0)
           {
            printf("Valid\n");
           }else printf("Invalid\n");

    return 0;
}
