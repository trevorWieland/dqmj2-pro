#include "context.h"

extern u8 native_data_0221c140[];
extern void native_fn_02202eb0(u32 base, u32 mask, u32 first, u32 second);

/* Apply the tag to the record's 16-bit spans and latch it in +0x1a. */
void native_main_021fea34(u32 tag)
{
    u32 *record = *(u32 **)native_data_0221c140;

    native_fn_02202eb0(record[0], 0xffffffff, *(u16 *)((u8 *)record + 0x10),
                       tag + *(u16 *)((u8 *)record + 0x12));
    (*(u8 **)native_data_0221c140)[0x1a] = (u8)tag;
}
