#include "context.h"

extern void native_fn_0200e630(u32 *words, u32 count);
extern u32 native_fn_0200ee8c(u32 arg0, u32 arg1, u32 arg2, u32 arg3);

/* Package the selector in `value` and the two-byte parameter in `param` as a
   two-word command transfer. */
u32 native_main_0200e6f0(u32 value, u32 param)
{
    u32 words[2];
    u32 status;

    words[0] = 0x03006000;
    native_fn_0200e630(words, 1);
    do {
        status = native_fn_0200ee8c(0, 2, 0, 1);
    } while (status != 1);
    words[0] = (value & 0xff) | 0x6200 | 0x02000000;
    words[1] = 0x01010000 | (param & 0xffff);
    native_fn_0200e630(words, 2);
    return 0;
}
