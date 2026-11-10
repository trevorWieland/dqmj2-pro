#include "context.h"

/* Report whether the current phase is one of the three moving phases. */
s32 native_ov000_021e0f58(void)
{
    switch (native_data_ov000_022322d4.field_278) {
    case 2:
    case 3:
    case 4:
        return 1;
    default:
        return 0;
    }
}
