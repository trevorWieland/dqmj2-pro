#include "context.h"

/* native_ov001_021df640.c: 64 bytes at 0x021df640 in ov001.
 * s32 func(void): after the mode probe, publish 0x36 (busy) or 0x28 (idle)
 * into the 0x022388ec +8 state byte. */
s32 native_ov001_021df640(void)
{
    if (native_fn_ov001_0220e2f0() != 0) {
        if (native_fn_ov001_021dda80() != 0)
            native_data_ov001_022388ec[8] = 0x36;
        else
            native_data_ov001_022388ec[8] = 0x28;
    }
    return 0;
}
