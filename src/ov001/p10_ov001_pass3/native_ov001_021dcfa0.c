#include "context.h"

/* native_ov001_021dcfa0.c: 84 bytes at 0x021dcfa0 in ov001.
 * s32 func(u8 *record): first of 0x3c bits that 0x021dcf0c reports, -1 when
 * the record is rejected or no bit is set. */
s32 native_ov001_021dcfa0(u8 *record)
{
    s32 i;

    if (ov001_record_is_active_021db8d0(record) == 0)
        goto fail;
    i = 0;
    do {
        if (native_fn_ov001_021dcf0c(record, i) != 0) {
            native_fn_ov001_021dcf54(record, i);
            return i;
        }
        i++;
    } while (i < 0x3c);
fail:
    return -1;
}
