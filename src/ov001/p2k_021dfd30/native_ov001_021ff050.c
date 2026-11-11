#include "context.h"

/* Rebind the caller's handle to the slot its record reports, then apply the
 * caller's selection unless the record caps it. */
void native_ov001_021ff050(s32 arg0, s32 arg1)
{
    u8 mode = *(u8 *)(native_fn_02065d88(arg0) + 0x2F);
    u8 limit = *(u8 *)(native_fn_02065d88(arg0) + 0x30);

    native_fn_ov001_0220b738(mode);
    native_fn_ov001_0220b75c(arg0);
    if (limit != 0)
        arg1 = 4;
    native_fn_ov001_0220b780(arg1);
}
