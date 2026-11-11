#include "context.h"

/* Same mirror-byte flip as its 0-state sibling, for the state-2 edge, and
 * advance the state byte to 3. */
s32 native_ov001_02210dd0(void)
{
    s32 result;

    if (native_data_ov001_0223e118[0] == 2) {
        native_data_ov001_0223e118[1] = 0;
        result = 1;
    } else {
        native_data_ov001_0223e118[1] =
            0x20 - *(s8 *)(native_data_ov001_0223e118 + 1);
        result = 0;
    }
    native_data_ov001_0223e118[0] = 3;
    return result;
}
