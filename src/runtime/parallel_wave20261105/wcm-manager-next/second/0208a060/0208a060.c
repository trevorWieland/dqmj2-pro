#include "context.h"
s32 native_main_0208a060(void)
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
    case WCM_PHASE_DCF:
        break;
    case WCM_PHASE_DCF_TO_IDLE:
        (void)native_fn_02008008(e);
        return WCM_RESULT_PROGRESS;
    case WCM_PHASE_IDLE:
        (void)native_fn_02008008(e);
        return WCM_RESULT_SUCCESS;
    default:
        WCMi_Warning(wcmWarningText_IllegalPhase, native_data_021cfcb4->phase);
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    if (native_data_021cfcb4->resetting == WCM_RESETTING_ON)
    {
        native_fn_0208a5ac(WCM_PHASE_DCF_TO_IDLE);
        native_data_021cfcb4->notifyId = WCM_NOTIFY_DISCONNECT;
    }
    else
    {
        WMErrCode   wmResult;
        wmResult = native_fn_020133f4(native_fn_0208ae50);
        switch (wmResult)
        {
        case WM_ERRCODE_OPERATING:
            native_fn_0208a5ac(WCM_PHASE_DCF_TO_IDLE);
            native_data_021cfcb4->notifyId = WCM_NOTIFY_DISCONNECT;
            break;
        case WM_ERRCODE_FIFO_ERROR:
            WCMi_Printf(wcmReportText_WmSyncError, "native_fn_020133f4", wmResult);
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
