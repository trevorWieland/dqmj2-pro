#include "context.h"

/* native_ov001_0220b7b8.c: 80 bytes at 0x0220b7b8 in ov001.
 * s32 func(void): arm the 0x10/2 timer, route on the 4-mode probe and raise
 * the 0x0223e088 +3 flag, reporting success. */
s32 native_ov001_0220b7b8(void)
{
    s32 value;
    s32 mode;

    native_fn_ov001_021f1294(0x10, 2);
    value = native_fn_ov001_0220b74c();
    mode = native_fn_ov001_0220b794();
    if (mode == 4) {
        native_fn_ov001_021e1358(value);
    } else {
        native_fn_ov001_021db438(value, mode);
        native_fn_ov001_021ee9fc();
    }
    native_data_ov001_0223e088[3] = 1;
    return 1;
}
