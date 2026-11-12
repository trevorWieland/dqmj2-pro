#include "context.h"

/* native_ov001_02219978.c: 64 bytes at 0x02219978 in ov001.
 * s32 func(Record *record): compare 0x021dbd24 against a tenth of 0x021dbcbc. */
s32 native_ov001_02219978(u8 **record)
{
    u8 *entry = *record;
    s32 high = native_fn_ov001_021dbd24(entry);
    s32 low = native_fn_ov001_021dbcbc(entry);

    return high <= low / 10;
}
