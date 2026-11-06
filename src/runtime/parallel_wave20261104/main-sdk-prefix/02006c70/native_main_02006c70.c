#include "context_00.h"
u32 native_main_02006c70 (void)
{
    OSIntrMode enabled = native_fn_02007ff4();
    u32 count;
    if (native_data_main_020e33c0.field_0004 < (u32)(0 - 1)) {
        count = native_data_main_020e33c0.field_0004++;
    }
    (void)native_fn_02008008(enabled);
    return count;
}
