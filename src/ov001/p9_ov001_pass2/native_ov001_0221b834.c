#include "context.h"

/*
 * native_ov001_0221b834.c: 96 bytes at 0x0221b834 in ov001 (base 0x021d7240).
 *
 * s32 func(Record8 *record)
 *
 * Same scan with three ANDed status bytes +0x3f/+0x40/+0x41.
 */
typedef struct {
    u8 unknown0[8];
    u8 *slot;
} Record8;

extern s32 native_fn_ov001_021db8d0(u8 *entry);

s32 native_ov001_0221b834(Record8 *record)
{
    s32 i = 0;
    u8 *entry = record->slot;

    do {
        if (native_fn_ov001_021db8d0(entry) != 0) {
            if (((s8 *)(entry + 0x200))[0x3f] == 0
                && ((s8 *)(entry + 0x200))[0x40] == 0
                && ((s8 *)(entry + 0x200))[0x41] == 0)
                break;
        }
        if (i == 2)
            return 1;
        i++;
        entry += 0x440;
    } while (i < 3);
    return 0;
}
