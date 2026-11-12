#include "context.h"

/* native_ov001_021df9a8.c: 60 bytes at 0x021df9a8 in ov001.
 * s32 func(void): advance the 0x0220b70c stage and publish 0x1f or 0x14 into
 * the 0x022388ec +8 state byte. */
s32 native_ov001_021df9a8(void)
{
    native_fn_ov001_0220b70c(1);
    if (native_fn_ov001_021de590() != 0) {
        native_data_ov001_022388ec[8] = 0x1f;
    } else {
        native_fn_ov001_021f9588();
        native_data_ov001_022388ec[8] = 0x14;
    }
    return 1;
}
