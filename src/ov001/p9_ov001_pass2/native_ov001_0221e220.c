#include "context.h"

/*
 * native_ov001_0221e220.c: 88 bytes at 0x0221e220 in ov001 (base 0x021d7240).
 *
 * s32 func(Record8 *record)
 *
 * Same scan, but the exit test reads the object pointer at record+0x1e8:
 * its halfword at +0xca must be set and its byte at +0xb1 clear.
 */
typedef struct {
    u8 unknown0[8];
    u8 *slot;
} Record8;

extern s32 ov001_record_is_active_021db8d0(u8 *entry);

s32 native_ov001_0221e220(Record8 *record)
{
    s32 i = 0;
    u8 *entry = record->slot;

    do {
        if (ov001_record_is_active_021db8d0(entry) != 0) {
            u8 *object = *(u8 **)(entry + 0x1e8);

            if (*(u16 *)(object + 0xca) != 0 && object[0xb1] == 0)
                break;
        }
        if (i == 2)
            return 1;
        i++;
        entry += 0x440;
    } while (i < 3);
    return 0;
}
