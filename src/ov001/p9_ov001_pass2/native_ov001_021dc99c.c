#include "context.h"

/*
 * native_ov001_021dc99c.c: 56 bytes at 0x021dc99c in ov001 (base 0x021d7240).
 *
 * s32 func(u8 *record)
 *
 * Counts the 0x3c records the overlay predicate accepts.  The declaration
 * order i-then-count with the count initialised first is what puts the
 * counter in r5 and the index in r4; i++ runs before the predicated count++
 * and the loop is a do/while so the call is the first body instruction.
 */
extern s32 native_fn_ov001_021dc940(u8 *record, s32 index);

s32 native_ov001_021dc99c(u8 *record)
{
    s32 i;
    s32 count;

    count = 0;
    i = 0;
    do {
        s32 result = native_fn_ov001_021dc940(record, i);

        i++;
        if (result != 0)
            count++;
    } while (i < 0x3c);
    return count;
}
