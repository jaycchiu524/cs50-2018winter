#define _XOPEN_SOURCE
#include <unistd.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>


int main(int argc, string argv[])
{
    for (int i = 1; i < argc; i++)
    {
        //Get string of hash which is a 13-character string
        if (strlen(argv[i]) != 13)
        {
            printf("Usage: ./crack hash\n");
            return 1;
        }

        //Define salt is equivalent to the first two characters of hash
        char salt[3];
        salt[0] = argv[i] [0];
        salt[1] = argv[i] [1];
        salt[2] = '\0';

        //List out all the possible characters of password
        //List vowel letters first to make the progress faster
        string letters = "\0aeiouAEIOUbcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ";

        //Define password which is not more than 5 characters and all alphabets
        char password[6] = "\0\0\0\0\0\0";

        //Cannot use strlen(letters), because the value would be 0 as '\0' is the first character
        for (int fifth = 0; fifth < 57; fifth++)
        {
            for (int fourth = 0; fourth < 57; fourth++)
            {
                for (int third = 0; third < 57; third++)
                {
                    for (int second = 0; second < 57; second++)
                    {
                        for (int first = 1; first < 57; first++)
                        {
                            password[0] = letters[first];
                            password[1] = letters[second];
                            password[2] = letters[third];
                            password[3] = letters[fourth];
                            password[4] = letters[fifth];

                            if (strcmp(crypt(password, salt), argv[i]) == 0)
                            {
                                printf("password %i= %s\n", i, password);

                            }

                        }
                    }
                }
            }
        }
    }
}
/*
brian:51.xJagtPnb6s
bjbrown:50GApilQSG3E2
emc:502sDZxA/ybHs
greg:50C6B0oz0HWzo
jana:50WUNAFdX/yjA
lloyd:50n0AAUD.pL8g
malan:50CcfIk1QrPr6
natmelo:50JIIyhDORqMU
rob:51v3Nh6ZWGHOQ
veronica:61v1CDwwP95bY
walker:508ny6Rw0aRio
zamyla:50cI2vYkF0YU2
*/


