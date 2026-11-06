#include "context.h"
s32 native_main_02089b64(void)
{
    OSIntrMode  e = native_fn_02007ff4();
    if (native_data_021cfcb4 == NULL)
    {
        WCMi_Warning(wcmWarningText_NotInit);
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    if (native_data_021cfcb4->phase != WCM_PHASE_WAIT)
    {
        WCMi_Warning(wcmWarningText_IllegalPhase, native_data_021cfcb4->phase);
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    native_data_021cfcb4 = NULL;
    (void)native_fn_02008008(e);
    return WCM_RESULT_SUCCESS;
}
