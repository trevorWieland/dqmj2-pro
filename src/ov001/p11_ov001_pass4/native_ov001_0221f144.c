#include "context.h"

/* native_ov001_0221f144.c: 88 bytes at 0x0221f144 in ov001.
 * s32 func(Record *record): 0x440-stride scan; 0x021db8d0 accepts and
 * 0x02218524 rejects with the 0x2000000 flag, with the i == 2 exit before
 * the advance. */
typedef struct {
    u8 unknown0[8];
    u8 *entries;
} Record;

s32 native_ov001_0221f144(Record *record)
{
    s32 i = 0;
    u8 *entry = record->entries;

    do {
        if (native_fn_ov001_021db8d0(entry) != 0) {
            if (native_fn_ov001_02218524(entry, 0x2000000) != 0)
                break;
        }
        if (i == 2)
            return 1;
        i++;
        entry += 0x440;
    } while (i < 3);
    return 0;
}
