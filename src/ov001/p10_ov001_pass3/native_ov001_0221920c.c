#include "context.h"

/* native_ov001_0221920c.c: 80 bytes at 0x0221920c in ov001.
 * s32 func(Record *record): two or more of the three live records accepted by
 * 0x021db8d0. */
typedef struct {
    u8 unknown0[8];
    u8 *entries;
} Record;

s32 native_ov001_0221920c(Record *record)
{
    s32 count = 0;
    s32 i;
    u8 *entry = record->entries;

    if (native_fn_ov001_022191e8() != 0) {
        i = 0;
        do {
            if (ov001_record_is_active_021db8d0(entry) != 0)
                count++;
            i++;
            entry += 0x440;
        } while (i < 3);
        if (count >= 2)
            return 1;
    }
    return 0;
}
