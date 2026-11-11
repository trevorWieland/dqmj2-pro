#include "context.h"

/* Move the battle record from state 1 to state 4 and signal its peer through
 * +0x24.  Returns 1 when the transition happened, 0 when the state was not 1. */
s32 native_ov001_02212af8(void)
{
    u8 *record = native_fn_ov001_021f1a44();
    u32 state = *(u32 *)(record + 0x2C);
    u8 *peer = *(u8 **)(record + 0x40);

    if (state != 1)
        return 0;
    *(u32 *)(record + 0x2C) = 4;
    *(u32 *)(peer + 0x24) = 1;
    return 1;
}
