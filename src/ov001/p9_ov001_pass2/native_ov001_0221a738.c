#include "context.h"

/*
 * native_ov001_0221a738.c: 88 bytes at 0x0221a738 in ov001 (base 0x021d7240).
 *
 * s32 func(Record4 *record)
 *
 * Three-entry scan of 0x440-stride records.  The +0x200 sub-block is a
 * common subexpression of both status-byte tests; writing it once is what
 * puts the add result in r0 and the loaded byte in r1, matching the image.
 * Status +0x4c == 0 && +0x45 == 0 ends the scan with 0.
 */
typedef struct {
    u8 unknown0[4];
    u8 *slot;
} Record4;

extern s32 ov001_record_is_active_021db8d0(u8 *entry);

s32 native_ov001_0221a738(Record4 *record)
{
    s32 i = 0;
    u8 *entry = record->slot;

    do {
        if (ov001_record_is_active_021db8d0(entry) != 0) {
            if (((s8 *)(entry + 0x200))[0x4c] == 0
                && ((s8 *)(entry + 0x200))[0x45] == 0)
                break;
        }
        if (i == 2)
            return 1;
        i++;
        entry += 0x440;
    } while (i < 3);
    return 0;
}
