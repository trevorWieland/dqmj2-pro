#include "context.h"

extern u8 native_data_0221c160[];

/* Resolve the indexed record when its enable bit is set. */
u32 native_main_022011b0(u32 index)
{
    u16 *record = (u16 *)*(u32 **)native_data_0221c160;

    if ((record[1] & (1 << index)) != 0)
        return (u32)((u8 *)record + 0x0e) + (index - 1) * 0x1e;
    return 0;
}
