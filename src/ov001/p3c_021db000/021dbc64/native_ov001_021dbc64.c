#include "../context.h"

/* Same mode-coded rescale as 0x021dbc18 with the additive offsets the original
   uses: modes >= 2 give (value << 1) + 16, mode 1 gives ((value * 3) >> 1) + 8,
   mode -1 halves, modes <= -2 quarter, any other mode leaves the value alone. */
s32 native_ov001_021dbc64(u32 a, u32 b, s32 value) {
    s8 mode;

    mode = *(s8 *)(a + b + 0x200 + 44);
    if (mode >= 2) {
        value = (value << 1) + 16;
    } else if (mode == 1) {
        value = ((value * 3) >> 1) + 8;
    } else if (mode == -1) {
        value = value >> 1;
    } else if (mode <= -2) {
        value = value >> 2;
    }
    return value;
}
