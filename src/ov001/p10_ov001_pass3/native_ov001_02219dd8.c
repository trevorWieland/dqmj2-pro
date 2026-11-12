#include "context.h"

/* native_ov001_02219dd8.c: 80 bytes at 0x02219dd8 in ov001.
 * s32 func(Record *record): same two-of-three count with 0x02219d8c. */
typedef struct {
    u8 unknown0[8];
    u8 *entries;
} Record;

s32 native_ov001_02219dd8(Record *record)
{
    s32 i;
    s32 count = 0;
    u8 *entry = record->entries;

    if (native_fn_ov001_02219d8c() != 0) {
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
