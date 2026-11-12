#include "context.h"

/* native_ov001_021dfa84.c: 64 bytes at 0x021dfa84 in ov001.
 * s32 func(void): after the mode probe, publish 0x36 (busy) or 4 (idle) into
 * the 0x022388ec +8 state byte. */
s32 native_ov001_021dfa84(void)
{
    if (native_fn_ov001_0220d278() != 0) {
        if (native_fn_ov001_021dda80() != 0)
            native_data_ov001_022388ec[8] = 0x36;
        else
            native_data_ov001_022388ec[8] = 4;
    }
    return 0;
}
