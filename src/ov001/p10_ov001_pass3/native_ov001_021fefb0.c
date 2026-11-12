#include "context.h"

/* native_ov001_021fefb0.c: 80 bytes at 0x021fefb0 in ov001.
 * s32 func(s32 mode, s32 value, s32 flag): submit a command through 0x0206c718
 * with a stack word and the mode byte. */
s32 native_ov001_021fefb0(s32 mode, s32 value, s32 flag)
{
    s32 byte;

    if (flag != 0) {
        byte = 0xc;
    } else {
        byte = mode == 1 ? 0x7f : 6;
        byte &= 0xff;
    }
    return native_fn_0206c718(*(s32 *)(native_data_ov001_02239c10 + 0x24),
                              1, value, flag, 0, byte);
}
