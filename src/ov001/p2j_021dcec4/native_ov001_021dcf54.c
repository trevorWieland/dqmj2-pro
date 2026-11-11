#include "context.h"

/* Clear one recorded flag in the caller's bitmap. */
void native_ov001_021dcf54(s32 arg0, s32 index)
{
    if (native_fn_ov001_021db8d0() == 0)
        return;
    *(u8 *)(arg0 + 0x3ED + index / 8) &= ~(1 << (index % 8));
}
