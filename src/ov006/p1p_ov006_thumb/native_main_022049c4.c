#include "context.h"

extern u8 native_data_0221c1e8[];

/* Store the byte at record offset 0x38 of the indexed 0x40-byte entry. */
void native_main_022049c4(u32 index, u8 value)
{
    *(u8 *)((u8 *)*(u32 **)native_data_0221c1e8 + index * 0x40 + 0x38) = value;
}
