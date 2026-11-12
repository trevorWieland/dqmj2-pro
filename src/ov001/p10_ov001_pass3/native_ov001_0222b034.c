#include "context.h"

/* native_ov001_0222b034.c: 52 bytes at 0x0222b034 in ov001.
 * void func(Record *record): route on the +0x2d byte of the +0x1fd lookup;
 * value 4 uses 0x02226d08, everything else 0x0222b198. */
typedef struct {
    u8 unknown0[0];
} Record;

void native_ov001_0222b034(u8 **record)
{
    u8 *state = (u8 *)native_fn_02065d88(((u8 *)*record)[0x1fd]);

    if (state[0x2d] == 4)
        native_fn_ov001_02226d08(record);
    else
        native_fn_ov001_0222b198(record);
}
