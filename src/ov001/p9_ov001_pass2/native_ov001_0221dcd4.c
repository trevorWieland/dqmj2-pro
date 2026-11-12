#include "context.h"

/*
 * native_ov001_0221dcd4.c: 88 bytes at 0x0221dcd4 in ov001 (base 0x021d7240).
 *
 * s32 func(Record4 *record)
 *
 * Same scan but the exit test is the OR form: either status byte +0x35 or
 * +0x36 being set ends the scan with 0.
 */
typedef struct {
    u8 unknown0[4];
    u8 *slot;
} Record4;

extern s32 native_fn_ov001_021db8d0(u8 *entry);

s32 native_ov001_0221dcd4(Record4 *record)
{
    s32 i = 0;
    u8 *entry = record->slot;

    do {
        if (native_fn_ov001_021db8d0(entry) != 0) {
            if (((s8 *)(entry + 0x200))[0x35] != 0
                || ((s8 *)(entry + 0x200))[0x36] != 0)
                break;
        }
        if (i == 2)
            return 1;
        i++;
        entry += 0x440;
    } while (i < 3);
    return 0;
}
