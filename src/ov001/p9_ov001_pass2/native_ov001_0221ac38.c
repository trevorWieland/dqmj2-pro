#include "context.h"

/*
 * native_ov001_0221ac38.c: 64 bytes at 0x0221ac38 in ov001 (base 0x021d7240).
 *
 * s32 func(Record4 *record)
 *
 * Three-entry scan of 0x440-stride records reached through the caller's
 * +4 pointer.  A record whose +0x31c and +0x1ff bytes are both set ends
 * the scan with 0; finishing all three returns 1 (the i == 2 test is the
 * last entry).  break shares the trailing return-0 epilogue.
 */
typedef struct {
    u8 unknown0[4];
    u8 *slot;
} Record4;

s32 native_ov001_0221ac38(Record4 *record)
{
    s32 i = 0;
    u8 *entry = record->slot;

    do {
        if (entry[0x31c] != 0 && entry[0x1ff] != 0)
            break;
        if (i == 2)
            return 1;
        i++;
        entry += 0x440;
    } while (i < 3);
    return 0;
}
