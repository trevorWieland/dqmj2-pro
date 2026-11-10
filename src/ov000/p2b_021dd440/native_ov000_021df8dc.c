#include "context.h"

/* Register one 20-byte record from the fifth source table in the first free
   slot of the 0x02231d24 block. Returns 1 when the device is busy, otherwise
   the initial 0. */
s32 native_ov000_021df8dc(s32 index)
{
    s32 result = 0;

    if (native_fn_ov000_021df748() != 0) {
        result = 1;
    } else {
        s32 slot = native_fn_ov000_021df77c();

        if (slot >= 0) {
            native_data_ov000_02231d24[slot].index = index;
            *(Payload20 *)&native_data_ov000_02231d28[slot] = native_data_ov000_02231bf0[4][index];
        }
    }
    return result;
}
