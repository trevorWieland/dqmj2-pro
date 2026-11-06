#include "context.h"
u32 native_main_0208e7f8(const u8 *text,const u8 **end)
{
    u32 value;
    u8 digit;
    *end=text;
    for(value=0;;){digit=(u8)(*text-48);if(digit>9)break;value=value*10+digit;*end=++text;}
    return value;
}
