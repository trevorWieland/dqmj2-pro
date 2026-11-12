#include "context.h"

/*
 * native_ov001_021e2aa4.c: 88 bytes at 0x021e2aa4 in ov001 (base 0x021d7240).
 *
 * s32 func(s32 type)
 *
 * Type-code dispatch over five signed-byte fields of one state block.  The
 * chain is linear (no jump table): 4, 1, 8, 0x10, 0x20, else 0.
 */
extern s8 native_data_ov001_022388ec[];

s32 native_ov001_021e2aa4(s32 type)
{
    if (type == 4)
        return native_data_ov001_022388ec[0x13];
    if (type == 1)
        return native_data_ov001_022388ec[0x27];
    if (type == 8)
        return native_data_ov001_022388ec[0x14];
    if (type == 0x10)
        return native_data_ov001_022388ec[0x15];
    if (type == 0x20)
        return native_data_ov001_022388ec[0x16];
    return 0;
}
