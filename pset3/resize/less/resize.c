#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }

    //Convert n to integer
    int n = atoi (argv[1]);
    char *infile = argv[2];
    char *outfile= argv[3];

    //The limit of value n
    if (n > 100 || n < 1)
    {
        printf("The value of n must be between 1 and 100.\n");
        return 2;
    }

    //open the infile
    FILE *inptr = fopen(infile, "r");

    //In case the infile doesn't exist
    if (inptr == NULL)
    {
        printf("The file %s cannot be opened!",infile);
        return 3;
    }

    //Create and open a new outfile(empty)
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("The file %s cannot be created!",outfile);
        return 4;
    }

    //Read file header of infile. define bf and bf_new
    BITMAPFILEHEADER bf, bf_new;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    //copy all bf value to bf_new
    bf_new = bf;

    //Read info header of infile. define bi and bi_new
    BITMAPINFOHEADER bi, bi_new;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    //copy all bi value to bi_new
    bi_new = bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
        {
            fclose(inptr);
            fclose(outptr);
            printf("The format is not supported\n");
            return 5;
        }

    //Determine the new dimension, multiply the width and height by factor n
    bi_new.biWidth  = bi.biWidth * n;
    bi_new.biHeight = bi.biHeight * n;

    //Determine the new and old paddings
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) %4) % 4;
    int padding_new = (4 - (bi_new.biWidth * sizeof(RGBTRIPLE)) %4) % 4;

    //Determine the new image and file size
    bi_new.biSizeImage = (bi_new.biWidth * sizeof(RGBTRIPLE) + padding_new) * abs(bi_new.biHeight);
    bf_new.bfSize = sizeof(bf_new) + sizeof(bi_new) + bi_new.biSizeImage;

    fwrite(&bf_new, sizeof(BITMAPFILEHEADER), 1, outptr);

    fwrite(&bi_new, sizeof(BITMAPINFOHEADER), 1, outptr);

   // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {

        //iterate over a scanline for n times
        for (int j = 0; j < n; j++)
        {

            // iterate over pixels in scanline
            for (int k = 0; k < bi.biWidth; k++)
            {
                RGBTRIPLE rgb;

                fread(&rgb, sizeof(RGBTRIPLE), 1, inptr);

                for( int l = 0; l < n; l++)
                {
                    fwrite(&rgb, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // then add the new paddings
            for (int l = 0; l < padding_new; l++)
            {
                fputc(0x00, outptr);
            }

              // Return to the beginning of a scanline
            if (j < n - 1)
                fseek(inptr, -bi.biWidth * sizeof(RGBTRIPLE), SEEK_CUR);

        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
    }

    fclose(inptr);
    fclose(outptr);

    return 0;
}
