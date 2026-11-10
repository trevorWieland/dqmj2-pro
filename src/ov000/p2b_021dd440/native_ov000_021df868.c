#include "context.h"

/* Register one 20-byte record from the second source table in the first free
   slot of the 0x02231c04 block. Returns 1 when the device is busy, otherwise
   the initial 0. */
s32 native_ov000_021df868(s32 index)
{
    s32 result = 0;

    if (native_fn_ov000_021df69c() != 0) {
        result = 1;
    } else {
        s32 slot = native_fn_ov000_021df6d0();

        if (slot >= 0) {
            native_data_ov000_02231c04[slot].index = index;
            *(Payload20 *)&native_data_ov000_02231c08[slot] = native_data_ov000_02231bf0[1][index];
        }
    }
    return result;
}
