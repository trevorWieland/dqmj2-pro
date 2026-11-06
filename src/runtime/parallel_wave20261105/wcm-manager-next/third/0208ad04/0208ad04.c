#include "context.h"
void native_main_0208ad04(void* arg)
{
    WMCallback*     cb = (WMCallback*)arg;
    switch (cb->errcode)
    {
    case WM_ERRCODE_SUCCESS:
        if (native_data_021cfcb4->phase == WCM_PHASE_IRREGULAR)
        {
            WCMi_Printf(wcmReportText_WmDisconnected, "native_fn_02012d84");
            native_fn_0208a5ac(WCM_PHASE_DCF_TO_IDLE);
            native_fn_0208a698();
        }
        else
        {
            native_data_021cfcb4->authId = 0;
            native_fn_0208a5ac(WCM_PHASE_IDLE);
            native_fn_0208a550(WCM_RESULT_SUCCESS, &(native_data_021cfcb4->bssDesc), 0, 2109);
        }
        break;
    case WM_ERRCODE_FAILED:
    case WM_ERRCODE_ILLEGAL_STATE:
        WCMi_Printf(wcmReportText_WmAsyncError, "native_fn_02012d84", cb->errcode, cb->wlCmdID, cb->wlResult);
        native_fn_0208a5ac(WCM_PHASE_DCF_TO_IDLE);
        native_fn_0208a698();
        break;
    case WM_ERRCODE_WM_DISABLE:
        WCMi_Warning(wcmWarningText_InvalidWmState);
    default:
        native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
        native_fn_0208a550(WCM_RESULT_FATAL_ERROR, &(native_data_021cfcb4->bssDesc), 0, 2127);
    }
}
