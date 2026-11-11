#include "context.h"

/* Flip the 0x0223e118 block's mirror byte when its state byte is still 0 and
 * advance the state to 1.  Returns 1 for the transition and 0 otherwise. */
s32 native_ov001_02210d98(void)
{
    s32 result;

    if (native_data_ov001_0223e118[0] == 0) {
        native_data_ov001_0223e118[1] = 0;
        result = 1;
    } else {
        native_data_ov001_0223e118[1] =
            0x20 - *(s8 *)(native_data_ov001_0223e118 + 1);
        result = 0;
    }
    native_data_ov001_0223e118[0] = 1;
    return result;
}
