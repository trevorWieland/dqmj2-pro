#include "context.h"

/* Register one 20-byte record from the first source table in the first free slot
   of the 0x02231e44 block. Returns 1 when the device is busy, otherwise the
   initial 0. */
s32 native_ov000_021df7f4(s32 index)
{
    s32 result = 0;

    if (native_fn_ov000_021df5f0() != 0) {
        result = 1;
    } else {
        s32 slot = native_fn_ov000_021df624();

        if (slot >= 0) {
            native_data_ov000_02231e44[slot].index = index;
            *(Payload20 *)&native_data_ov000_02231e48[slot] = native_data_ov000_02231bf0[0][index];
        }
    }
    return result;
}
