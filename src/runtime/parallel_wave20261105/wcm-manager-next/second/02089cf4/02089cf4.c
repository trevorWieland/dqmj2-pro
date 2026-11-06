#include "context.h"
s32 native_main_02089cf4(void)
{
    OSIntrMode  e = native_fn_02007ff4();
    if (native_data_021cfcb4 == NULL)
    {
        WCMi_Warning(wcmWarningText_NotInit);
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    switch (native_data_021cfcb4->phase)
    {
    case WCM_PHASE_IDLE:
        break;
    case WCM_PHASE_IDLE_TO_WAIT:
        (void)native_fn_02008008(e);
        return WCM_RESULT_PROGRESS;
    case WCM_PHASE_WAIT:
        (void)native_fn_02008008(e);
        return WCM_RESULT_SUCCESS;
    default:
        WCMi_Warning(wcmWarningText_IllegalPhase, native_data_021cfcb4->phase);
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    {
        WMErrCode   wmResult;
        wmResult = native_fn_02012724(native_fn_0208a730);
        switch (wmResult)
        {
        case WM_ERRCODE_OPERATING:
            native_fn_0208a5ac(WCM_PHASE_IDLE_TO_WAIT);
            native_data_021cfcb4->notifyId = WCM_NOTIFY_CLEANUP;
            break;
        case WM_ERRCODE_FIFO_ERROR:
            WCMi_Printf(wcmReportText_WmSyncError, "native_fn_02012724", wmResult);
            (void)native_fn_02008008(e);
            return WCM_RESULT_REJECT;
        case WM_ERRCODE_ILLEGAL_STATE:
            WCMi_Warning(wcmWarningText_InvalidWmState);
        default:
            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
            (void)native_fn_02008008(e);
            return WCM_RESULT_FATAL_ERROR;
        }
    }
    (void)native_fn_02008008(e);
    return WCM_RESULT_ACCEPT;
}
