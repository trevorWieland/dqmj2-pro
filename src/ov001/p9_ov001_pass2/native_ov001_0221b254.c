#include "context.h"

/*
 * native_ov001_0221b254.c: 88 bytes at 0x0221b254 in ov001 (base 0x021d7240).
 *
 * s32 func(Record4 *record)
 *
 * Same scan; the exit test is either unsigned byte +0x8d or +0x8e of the
 * object at record+0x1e8 being below 5.  The unsigned compare is what the
 * image's ldrbhs/cmphs pair proves.
 */
typedef struct {
    u8 unknown0[4];
    u8 *slot;
} Record4;

extern s32 native_fn_ov001_021db8d0(u8 *entry);

s32 native_ov001_0221b254(Record4 *record)
{
    s32 i = 0;
    u8 *entry = record->slot;

    do {
        if (native_fn_ov001_021db8d0(entry) != 0) {
            u8 *object = *(u8 **)(entry + 0x1e8);

            if (object[0x8d] < 5 || object[0x8e] < 5)
                break;
        }
        if (i == 2)
            return 1;
        i++;
        entry += 0x440;
    } while (i < 3);
    return 0;
}
