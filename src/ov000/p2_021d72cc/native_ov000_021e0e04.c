#include "context.h"

/* Report whether the current input mode is one of the three accepted layouts. */
s32 native_ov000_021e0e04(void)
{
    switch (native_fn_020404e0()) {
    case 3:
    case 4:
    case 5:
        return 1;
    default:
        return 0;
    }
}
