#include "context.h"

/* True while the selection byte at 0x02242ba0+2 is neither of the two inactive
 * modes (3 and 7).  The image returns 0 from the equality branch first, which is
 * the if/return form rather than a negated expression. */
s32 native_ov001_02215760(void)
{
    u8 mode = native_data_ov001_02242ba0[2];

    if (mode == 3 || mode == 7)
        return 0;
    return 1;
}
