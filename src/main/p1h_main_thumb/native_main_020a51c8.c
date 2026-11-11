#include "context.h"

extern void native_fn_02008be0(u32 fill, u8 *destination, u32 size);

/* Clear one 0x100-byte record and mark its last slot. */
void native_main_020a51c8(u8 *base, u32 index)
{
    u8 *record = base + (index << 8);

    native_fn_02008be0(0, record, 0x100);
    record[0xe7] = 0xff;
}
