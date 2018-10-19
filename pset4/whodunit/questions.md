# Questions

## What's `stdint.h`?

Library for Integer types like uint8_t etc.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

to specify the range of numbers you can use. u stands for unsigned and means you have no negative numbers

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE = 1 byte
DWORD = 4 bytes
LONG = 4 bytes
WORD = 2 bytes


## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

ASCII: B M

## What's the difference between `bfSize` and `biSize`?

bfSize is the Size of the whole bmp
biSize is the Size of the BITMAPINFOHEADER file

## What does it mean if `biHeight` is negative?

If biHeight is negative, the bitmap is a top-down DIB with the origin at the upper left corner

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If it can´t find a file

## Why is the third argument to `fread` always `1` in our code?

Specifies how many elements we want to read (1)

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?



## What does `fseek` do?

fseek() function is used to move file pointer position to the given location.

## What is `SEEK_CUR`?

It moves file pointer position to given location.

## Whodunit?

TODO
