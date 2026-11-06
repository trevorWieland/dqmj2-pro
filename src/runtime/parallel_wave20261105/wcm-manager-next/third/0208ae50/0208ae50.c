#include "context.h"
void native_main_0208ae50(void* arg)
{
    WMCallback*     cb = (WMCallback*)arg;
    WMErrCode       wmResult = WM_ERRCODE_MAX;
    switch (cb->errcode)
    {
    case WM_ERRCODE_SUCCESS:
        if (native_data_021cfcb4->phase == WCM_PHASE_IRREGULAR)
        {
            native_fn_0208a5ac(WCM_PHASE_DCF_TO_IDLE);
            native_fn_0208a698();
        }
        else
        {
            wmResult = native_fn_02012d84(native_fn_0208ad04, 0);
            switch (wmResult)
            {
            case WM_ERRCODE_OPERATING:
                break;
            case WM_ERRCODE_FIFO_ERROR:
                WCMi_Printf(wcmReportText_WmSyncError, "native_fn_02012d84", wmResult);
                native_fn_0208a5ac(WCM_PHASE_IRREGULAR);
                native_fn_0208a550(WCM_RESULT_FAILURE, &(native_data_021cfcb4->bssDesc), 0, 2228);
                break;
            case WM_ERRCODE_ILLEGAL_STATE:
                WCMi_Printf(wcmReportText_WmSyncError, "native_fn_02012d84", wmResult);
                native_fn_0208a5ac(WCM_PHASE_DCF_TO_IDLE);
                native_fn_0208a698();
                break;
            default:
                native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
                native_fn_0208a550(WCM_RESULT_FATAL_ERROR, &(native_data_021cfcb4->bssDesc), 0, 2240);
            }
        }
        break;
    case WM_ERRCODE_FAILED:
    case WM_ERRCODE_ILLEGAL_STATE:
        WCMi_Printf(wcmReportText_WmAsyncError, "native_fn_020133f4", cb->errcode, cb->wlCmdID, cb->wlResult);
        native_fn_0208a5ac(WCM_PHASE_DCF_TO_IDLE);
        native_fn_0208a698();
        break;
    case WM_ERRCODE_WM_DISABLE:
        WCMi_Warning(wcmWarningText_InvalidWmState);
    default:
        native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
        native_fn_0208a550(WCM_RESULT_FATAL_ERROR, &(native_data_021cfcb4->bssDesc), 0, 2259);
    }
}
