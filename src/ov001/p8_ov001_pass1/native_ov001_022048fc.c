#include "context.h"

/* Clear one bit of one word slot of the 12-byte record, returning the new word. */
u32 native_ov001_022048fc(s32 record, s32 slot, s32 bit)
{
    u32 *row = (u32 *)(native_data_ov001_0223d904 + record * 12);

    row[slot] &= ~(1u << bit);
    return row[slot];
}
