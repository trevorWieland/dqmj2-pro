#include "context.h"
s32 native_main_0208a268(void)
{
    OSIntrMode  e = native_fn_02007ff4();
    s32         phase = WCM_PHASE_NULL;
    if (native_data_021cfcb4 != NULL)
    {
        phase = (s32) (native_data_021cfcb4->phase);
    }
    (void)native_fn_02008008(e);
    return phase;
}
