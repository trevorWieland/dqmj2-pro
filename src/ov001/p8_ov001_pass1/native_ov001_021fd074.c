#include "context.h"
u8 *native_ov001_021fd074(s32 selector, s32 index)
{
    s8 extra = selector == 0 ? 0 : 3;
    return (u8 *)(native_data_ov001_02239ca4 + (index + extra) * 16);
}
