#include "context.h"

/* native_ov001_0222b0d0.c: 52 bytes at 0x0222b0d0 in ov001. */
void native_ov001_0222b0d0(u8 **record)
{
    u8 *state = (u8 *)native_fn_02065d88(((u8 *)*record)[0x1fd]);

    if (state[0x2d] == 4)
        native_fn_ov001_02226d08(record);
    else
        native_fn_ov001_02226ec8(record);
}

