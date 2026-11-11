#include "context.h"

/* Byte at `record * 100 + (offset - 1)` in the 100-byte-stride table whose base
 * pointer is stored at 0x02249828+4.  The `sub #1` is folded into the index
 * before the multiply-add, so the caller passes a one-based offset. */
u8 native_ov001_0222d91c(s32 record, s32 offset)
{
    u8 *table = *(u8 **)(native_data_ov001_02249828 + 4);

    return table[record * 100 + (offset - 1)];
}
