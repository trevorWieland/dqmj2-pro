#include "context.h"
void native_main_0208ab0c(void* arg)
{
    WMCallback*     cb = (WMCallback*)arg;
    switch (cb->errcode)
    {
    case WM_ERRCODE_SUCCESS:
        native_fn_0208a5ac(WCM_PHASE_IDLE);
        native_fn_0208a550(WCM_RESULT_SUCCESS, 0, 0, 1923);
        break;
    case WM_ERRCODE_FAILED:
        WCMi_Printf(wcmReportText_WmAsyncError, "WM_EndScan", cb->errcode, cb->wlCmdID, cb->wlResult);
        native_fn_0208a698();
        break;
    case WM_ERRCODE_ILLEGAL_STATE:
    case WM_ERRCODE_WM_DISABLE:
        WCMi_Warning(wcmWarningText_InvalidWmState);
    default:
        native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
        native_fn_0208a550(WCM_RESULT_FATAL_ERROR, 0, 0, 1939);
    }
}
