#include "../context.h"

/* Rescales `value` in place by the signed mode byte at (a + b + 0x22C): modes
   >= 2 double it, mode 1 gives (value * 3) >> 1, mode -1 halves it, modes <= -2
   quarter it, and any other mode leaves it alone. */
s32 native_ov001_021dbc18(u32 a, u32 b, s32 value) {
    s8 mode;

    mode = *(s8 *)(a + b + 0x200 + 44);
    if (mode >= 2) {
        value = value << 1;
    } else if (mode == 1) {
        value = (value * 3) >> 1;
    } else if (mode == -1) {
        value = value >> 1;
    } else if (mode <= -2) {
        value = value >> 2;
    }
    return value;
}
