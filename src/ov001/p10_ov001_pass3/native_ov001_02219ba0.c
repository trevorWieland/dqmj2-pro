#include "context.h"

/* native_ov001_02219ba0.c: 64 bytes at 0x02219ba0 in ov001.
 * s32 func(Record *record): same tenth comparison with 0x021dbd30/0x021dbcf0. */
s32 native_ov001_02219ba0(u8 **record)
{
    u8 *entry = *record;
    s32 high = ov001_record_field_1f2_021dbd30(entry);
    s32 low = native_fn_ov001_021dbcf0(entry);

    return high <= low / 10;
}
