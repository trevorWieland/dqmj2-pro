#include "context.h"

/* native_ov001_0221dd80.c: 52 bytes at 0x0221dd80 in ov001.
 * s32 func(Record *record): compare the +4 value against 3/2 of the +8 value. */
typedef struct {
    u8 unknown0[4];
    s32 value4;
    s32 value8;
} Record;

s32 native_ov001_0221dd80(Record *record)
{
    s32 high = native_fn_ov001_0221887c(record->value8);
    s32 low = native_fn_ov001_022188d0(record->value4);

    return low < high * 3 / 2;
}
