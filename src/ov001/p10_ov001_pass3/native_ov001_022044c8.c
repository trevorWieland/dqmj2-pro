#include "context.h"

/* native_ov001_022044c8.c: 84 bytes at 0x022044c8 in ov001.
 * s32 func(s32 handle, s32 flag, s32 a, s32 b): submit command 5 with the
 * 0x6f/0x7b mode byte and then commit handle 1. */
s32 native_ov001_022044c8(s32 handle, s32 flag, s32 a, s32 b)
{
    u32 mode = flag != 0 ? 0x6f : 0x7b;

    native_fn_0204b4f4(handle, a, b, 1, 5, mode & 0xff);
    native_fn_0204b61c(handle, 1);
    return 0;
}
