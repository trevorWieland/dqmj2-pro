#include "context.h"

/* native_ov001_0221c11c.c: 80 bytes at 0x0221c11c in ov001.
 * s32 func(Record *record): same scan with 0x021dbd30 as the second test. */
typedef struct {
    u8 unknown0[8];
    u8 *entries;
} Record;

s32 native_ov001_0221c11c(Record *record)
{
    s32 i = 0;
    u8 *entry = record->entries;

    do {
        if (native_fn_ov001_021db8d0(entry) != 0) {
            if (native_fn_ov001_021dbd30(entry) != 0)
                break;
        }
        if (i == 2)
            return 1;
        i++;
        entry += 0x440;
    } while (i < 3);
    return 0;
}
