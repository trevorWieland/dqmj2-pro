#include "context.h"

extern u8 native_data_020de7cc[];
extern u8 native_data_020de804[];
extern u8 native_data_021d1540[];

extern s32 native_fn_0208eb34(u32 handle);
extern u32 native_fn_0208ed2c(u32 address);

/* Bind the active resource to the shared slot when the query succeeds. */
s32 native_main_0208e9bc(void)
{
    u32 *root = *(u32 **)native_data_020de7cc;
    s32 result = native_fn_0208eb34(*(u32 *)((u8 *)root + 0x20));

    if (result >= 0)
        *(u32 *)(native_data_021d1540 + 0x0c) = native_fn_0208ed2c((u32)native_data_020de804);
    return result;
}
