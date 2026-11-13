#include "context.h"

/*
 * native_ov001_0221e1c8.c: 80 bytes at 0x0221e1c8 in ov001 (base 0x021d7240).
 *
 * s32 func(Record8 *record)
 *
 * Same scan; the exit test is the signed halfword at +0x28 of the object
 * pointer at record+0x1e8 reaching 10.
 */
typedef struct {
    u8 unknown0[8];
    u8 *slot;
} Record8;

extern s32 ov001_record_is_active_021db8d0(u8 *entry);

s32 native_ov001_0221e1c8(Record8 *record)
{
    s32 i = 0;
    u8 *entry = record->slot;

    do {
        if (ov001_record_is_active_021db8d0(entry) != 0) {
            s16 value = *(s16 *)(*(u32 *)(entry + 0x1e8) + 0x28);

            if (value >= 10)
                break;
        }
        if (i == 2)
            return 1;
        i++;
        entry += 0x440;
    } while (i < 3);
    return 0;
}
