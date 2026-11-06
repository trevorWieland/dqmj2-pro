#include "context.h"
s32 native_main_02089ba0(WCMConfig* config, WCMNotify notify)
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
    case WCM_PHASE_WAIT:
        native_fn_0208a328(config, notify);
        break;
    case WCM_PHASE_WAIT_TO_IDLE:
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
    {
        WMErrCode   wmResult;
        wmResult = native_fn_020115b4(native_data_021cfcb4->wmWork, (u16) native_data_021cfcb4->config.dmano);
        switch (wmResult)
        {
        case WM_ERRCODE_SUCCESS:
            break;
        case WM_ERRCODE_ILLEGAL_STATE:
            WCMi_Warning(wcmWarningText_InvalidWmState);
            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
            (void)native_fn_02008008(e);
            return WCM_RESULT_FATAL_ERROR;
        case WM_ERRCODE_WM_DISABLE:
            WCMi_Warning(wcmWarningText_UnsuitableArm7);
            (void)native_fn_02008008(e);
            return WCM_RESULT_WMDISABLE;
        case WM_ERRCODE_INVALID_PARAM:
        default:
            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
            (void)native_fn_02008008(e);
            return WCM_RESULT_FATAL_ERROR;
        }
        if (0 == native_fn_02012290())
        {
            if (WM_ERRCODE_SUCCESS != native_fn_020117c4())
            {
                native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
                (void)native_fn_02008008(e);
                return WCM_RESULT_FATAL_ERROR;
            }
            WCMi_Warning(wcmWarningText_WirelessForbidden);
            (void)native_fn_02008008(e);
            return WCM_RESULT_WMDISABLE;
        }
        wmResult = native_fn_02011f14(native_fn_0208a6d8);
        if (wmResult != WM_ERRCODE_SUCCESS)
        {
            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
            (void)native_fn_02008008(e);
            return WCM_RESULT_FATAL_ERROR;
        }
        wmResult = native_fn_02012630(native_fn_0208a730);
        switch (wmResult)
        {
        case WM_ERRCODE_OPERATING:
            native_fn_0208a5ac(WCM_PHASE_WAIT_TO_IDLE);
            native_data_021cfcb4->notifyId = WCM_NOTIFY_STARTUP;
            break;
        case WM_ERRCODE_FIFO_ERROR:
            WCMi_Printf(wcmReportText_WmSyncError, "native_fn_02012630", wmResult);
            native_fn_0208a5ac(WCM_PHASE_IRREGULAR);
            (void)native_fn_02008008(e);
            return WCM_RESULT_FAILURE;
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
