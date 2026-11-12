#include "context.h"

/* native_ov001_021e2984.c: 84 bytes at 0x021e2984 in ov001.
 * void func(u8 *record, s32 value): decrement the live +0x1a or +0x12 timer,
 * publish the two +0x31e/+0x31f mode bytes and raise +0x11. */
void native_ov001_021e2984(u8 *record, s32 value)
{
    if (native_data_ov001_022388ec[0xa] == 1)
        native_data_ov001_022388ec[0x12] -= 1;
    else
        native_data_ov001_022388ec[0x1a] -= 1;
    native_fn_ov001_021e82fc(value, record[0x31e], record[0x31f]);
    native_data_ov001_022388ec[0x11] = 1;
}
