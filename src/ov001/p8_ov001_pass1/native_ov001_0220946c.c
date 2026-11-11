#include "context.h"
s32 native_ov001_0220946c(u8 *base, s32 index)
{
    u8 *slot = base + index;
    if (*(s8 *)slot) {
        slot[0] = 0;
        slot[0x3C] = 0;
        return 1;
    }
    return 0;
}
