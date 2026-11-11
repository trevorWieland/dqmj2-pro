#include "context.h"

/* Four-value state test on the byte at +0x326: only states 1 through 4 are
 * live.  The jump table in the image is the compiler's dense-switch form. */
s32 native_ov001_021dc8b4(u8 *state)
{
    switch (state[0x326]) {
    case 1:
    case 2:
    case 3:
    case 4:
        return 1;
    default:
        return 0;
    }
}
