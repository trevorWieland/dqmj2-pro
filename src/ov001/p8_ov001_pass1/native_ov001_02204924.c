#include "context.h"

/* Test one bit of one word slot of the 12-byte record selected by the caller.
 * The shift count is a register because the image uses `and` with a shifted
 * register operand (`r1, lsl r2`), not an immediate mask. */
u32 native_ov001_02204924(s32 record, s32 slot, s32 bit)
{
    u32 *row = (u32 *)(native_data_ov001_0223d904 + record * 12);

    return row[slot] & (1u << bit);
}
