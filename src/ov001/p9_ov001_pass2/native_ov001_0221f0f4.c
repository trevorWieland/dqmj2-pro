#include "context.h"

/*
 * native_ov001_0221f0f4.c: 80 bytes at 0x0221f0f4 in ov001 (base 0x021d7240).
 *
 * s32 func(Record8 *record)
 *
 * Same scan; the exit test is status byte +0x54 being zero.
 */
typedef struct {
    u8 unknown0[8];
    u8 *slot;
} Record8;

extern s32 native_fn_ov001_021db8d0(u8 *entry);

s32 native_ov001_0221f0f4(Record8 *record)
{
    s32 i = 0;
    u8 *entry = record->slot;

    do {
        if (native_fn_ov001_021db8d0(entry) != 0) {
            if (((s8 *)(entry + 0x200))[0x54] == 0)
                break;
        }
        if (i == 2)
            return 1;
        i++;
        entry += 0x440;
    } while (i < 3);
    return 0;
}
