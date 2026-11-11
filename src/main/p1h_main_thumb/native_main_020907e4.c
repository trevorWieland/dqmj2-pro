#include "context.h"

/* Big-endian pack of one word into four bytes. */
void native_main_020907e4(u32 value, u8 *output)
{
    output[0] = (u8)(value >> 24);
    output[1] = (u8)(value >> 16);
    output[2] = (u8)(value >> 8);
    output[3] = (u8)value;
}
