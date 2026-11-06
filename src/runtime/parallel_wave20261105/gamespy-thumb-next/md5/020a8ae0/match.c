#include "context.h"
void native_main_020a8ae0 (unsigned char digest[16], char output[33])
{
unsigned int i;

    for (i = 0; i < 16; i++)
    {
        output[i*2  ] = hex_digits[digest[i] / 16];
        output[i*2+1] = hex_digits[digest[i] % 16];
    }
    output[32] = '\0';
}