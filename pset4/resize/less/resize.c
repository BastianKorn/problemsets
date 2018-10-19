#include <stdio.h>
#include <stdlib.h>
#include "bmp.h"

int main(int argc, char* argv[])
{
    if (argc != 4)
    {
        printf("Usage: ./resize factor infile outfile\n");
        return 1;
    }

    int factor = atoi(argv[1]);
    char* infile = argv[2];
    char* outfile = argv[3];

    if (factor < 1 || factor > 100)
    {
        printf("Factor must be in range of 1 to 100!\n");
        return 1;
    }

    // open infile to inptr for read
    FILE* inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open outfile to outptr for write
    FILE* outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not open %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER and copy to bf_resize
    BITMAPFILEHEADER bf, bf_resize;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bf_resize = bf;

    // read infile's BITMAPINFOHEADER and copy to bf_resize
    BITMAPINFOHEADER bi, bi_resize;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    bi_resize = bi;

    // copy new width and height to bi_resize
    bi_resize.biWidth  = bi.biWidth * factor;
    bi_resize.biHeight = bi.biHeight * factor;

    // old and new paddings
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) %4) % 4;
    int res_padding = (4 - (bi_resize.biWidth * sizeof(RGBTRIPLE)) %4) % 4;

    // new image sizes
    bi_resize.biSizeImage = (bi_resize.biWidth * sizeof(RGBTRIPLE) + res_padding) * abs(bi_resize.biHeight);
    bf_resize.bfSize = bf.bfSize - bi.biSizeImage + bi_resize.biSizeImage;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf_resize, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi_resize, sizeof(BITMAPINFOHEADER), 1, outptr);

    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // Read each scanline factor times
        for (int j = 0; j < factor; j++)
        {
            // iterate over pixels in scanline
            for (int k = 0; k < bi.biWidth; k++)
            {
                // temporary
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile, multiplied by factor
                for (int l = 0; l < factor; l++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // Add a new padding
            for (int l = 0; l < res_padding; l++)
            {
                fputc(0x00, outptr);
            }

            // Return to the beginning of a scanline
            if (j < factor - 1)
            {
                fseek(inptr, -bi.biWidth * sizeof(RGBTRIPLE), SEEK_CUR);
            }
        }

        // Skip over padding
        fseek(inptr, padding, SEEK_CUR);
    }

    fclose(inptr);
    fclose(outptr);
    return 0;
}
