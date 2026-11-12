#include "context.h"

/* native_ov001_021f74fc.c: 72 bytes at 0x021f74fc in ov001.
 * s32 func(void): run the +4 mode path or the table byte path, flush, then set
 * the 0x1b stage byte. */
s32 native_ov001_021f74fc(void)
{
    if ((native_fn_ov001_021e29e8() & 4) != 0) {
        native_fn_ov001_021e2a48(4);
    } else {
        u8 *entry = *(u8 **)(native_data_ov001_0223989c + 0x84);
        native_fn_ov001_021e29f8(4, entry[0x31e]);
    }
    native_fn_ov001_021e048c();
    native_data_ov001_0223989c[0x1b] = 0x1b;
    return 0;
}
