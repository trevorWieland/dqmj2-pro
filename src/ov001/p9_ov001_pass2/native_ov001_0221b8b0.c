#include "context.h"

/*
 * native_ov001_0221b8b0.c: 88 bytes at 0x0221b8b0 in ov001 (base 0x021d7240).
 *
 * s32 func(Record8 *record)
 *
 * Same shape through +8 with status bytes +0x42/+0x43.
 */
typedef struct {
    u8 unknown0[8];
    u8 *slot;
} Record8;

extern s32 ov001_record_is_active_021db8d0(u8 *entry);

s32 native_ov001_0221b8b0(Record8 *record)
{
    s32 i = 0;
    u8 *entry = record->slot;

    do {
        if (ov001_record_is_active_021db8d0(entry) != 0) {
            if (((s8 *)(entry + 0x200))[0x42] == 0
                && ((s8 *)(entry + 0x200))[0x43] == 0)
                break;
        }
        if (i == 2)
            return 1;
        i++;
        entry += 0x440;
    } while (i < 3);
    return 0;
}
