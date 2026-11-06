#include "context.h"
s32 native_main_0208a114(void)
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
    case WCM_PHASE_DCF:
    case WCM_PHASE_IRREGULAR:
        break;
    case WCM_PHASE_TERMINATING:
        (void)native_fn_02008008(e);
        return WCM_RESULT_PROGRESS;
    case WCM_PHASE_WAIT:
        (void)native_fn_02008008(e);
        return WCM_RESULT_SUCCESS;
    case WCM_PHASE_SEARCH:
        native_fn_0208a5ac(WCM_PHASE_TERMINATING);
        native_data_021cfcb4->notifyId = WCM_NOTIFY_TERMINATE;
        (void)native_fn_02008008(e);
        return WCM_RESULT_ACCEPT;
    case WCM_PHASE_WAIT_TO_IDLE:
    case WCM_PHASE_IDLE_TO_WAIT:
    case WCM_PHASE_IDLE_TO_SEARCH:
    case WCM_PHASE_SEARCH_TO_IDLE:
    case WCM_PHASE_IDLE_TO_DCF:
    case WCM_PHASE_DCF_TO_IDLE:
    case WCM_PHASE_FATAL_ERROR:
    default:
        WCMi_Warning(wcmWarningText_IllegalPhase, native_data_021cfcb4->phase);
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    if (native_data_021cfcb4->resetting == WCM_RESETTING_ON)
    {
        native_fn_0208a5ac(WCM_PHASE_TERMINATING);
        native_data_021cfcb4->notifyId = WCM_NOTIFY_TERMINATE;
    }
    else
    {
        WMStatusPrefix*   ws;
        u16         wmState;
        WMErrCode   wmResult;
        ws = (WMStatusPrefix*)native_fn_02011e90();
        native_fn_020072d0(ws, 2);
        wmState = ws->state;
        switch (wmState)
        {
        case WM_STATE_READY:
            wmResult = native_fn_020117c4();
            if (wmResult == WM_ERRCODE_SUCCESS)
            {
                native_fn_0208a5ac(WCM_PHASE_WAIT);
                native_data_021cfcb4->notifyId = WCM_NOTIFY_COMMON;
                (void)native_fn_02008008(e);
                return WCM_RESULT_SUCCESS;
            }
            break;
        case WM_STATE_STOP:
            wmResult = native_fn_020126a4(native_fn_0208a730);
            break;
        case WM_STATE_IDLE:
            wmResult = native_fn_02012724(native_fn_0208a730);
            break;
        default:
            native_data_021cfcb4->resetting = WCM_RESETTING_ON;
            wmResult = native_fn_020127ec(native_fn_0208af1c);
        }
        switch (wmResult)
        {
        case WM_ERRCODE_OPERATING:
            native_fn_0208a5ac(WCM_PHASE_TERMINATING);
            native_data_021cfcb4->notifyId = WCM_NOTIFY_TERMINATE;
            break;
        case WM_ERRCODE_FIFO_ERROR:
            WCMi_Printf(wcmReportText_WmSyncError, "WM_***", wmResult);
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
