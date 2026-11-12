#include "context.h"

/* native_ov001_0221490c.c: 64 bytes at 0x0221490c in ov001.
 * s32 func(void): arm the 0x10/2 timer, publish the +0x31e state test and
 * raise the +3 flag, reporting success. */
s32 native_ov001_0221490c(void)
{
    u8 *entry;

    native_fn_ov001_021f1294(0x10, 2);
    entry = *(u8 **)(native_data_ov001_02242b94 + 8);
    native_fn_ov001_021e1358(entry[0x31e] == 0);
    native_data_ov001_02242b94[3] = 1;
    return 1;
}
