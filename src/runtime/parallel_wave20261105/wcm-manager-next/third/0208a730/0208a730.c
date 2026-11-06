#include "context.h"
void native_main_0208a730(void* arg)
{
    WMCallback*     cb = (WMCallback*)arg;
    WMErrCode       wmResult = WM_ERRCODE_MAX;
    switch (cb->errcode)
    {
    case WM_ERRCODE_SUCCESS:
        switch (cb->apiid)
        {
        case WM_APIID_ENABLE:
            wmResult = native_fn_020126e4(native_fn_0208a730);
            break;
        case WM_APIID_DISABLE:
            wmResult = native_fn_020117c4();
            switch (wmResult)
            {
            case WM_ERRCODE_SUCCESS:
                native_fn_0208a5ac(WCM_PHASE_WAIT);
                native_fn_0208a550(WCM_RESULT_SUCCESS, 0, 0, 1635);
                break;
            case WM_ERRCODE_WM_DISABLE:
                WCMi_Warning(wcmWarningText_InvalidWmState);
            default:
                native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
                native_fn_0208a550(WCM_RESULT_FATAL_ERROR, 0, 0, 1644);
            }
            return;
        case WM_APIID_POWER_ON:
            native_fn_0208a5ac(WCM_PHASE_IDLE);
            native_fn_0208a550(WCM_RESULT_SUCCESS, 0, 0, 1651);
            return;
        case WM_APIID_POWER_OFF:
            wmResult = native_fn_020126a4(native_fn_0208a730);
            break;
        case WM_APIID_SET_LIFETIME:
            wmResult = native_fn_020141b0(native_fn_0208a730, 0);
            break;
        case WM_APIID_SET_BEACON_IND:
            wmResult = native_fn_0201407c(native_fn_0208a730, (u16) (native_data_021cfcb4->wepDesc.mode), (u16) (native_data_021cfcb4->wepDesc.keyId),
                                      (const u8*)(native_data_021cfcb4->wepDesc.key));
            break;
        case WM_APIID_SET_WEPKEY_EX:
            wmResult = native_fn_02012cb8(native_fn_0208ab60, &(native_data_021cfcb4->bssDesc), NULL,
                                         ((native_data_021cfcb4->option & WCM_OPTION_MASK_POWER) == WCM_OPTION_POWER_ACTIVE ? FALSE : TRUE),
                                         ((native_data_021cfcb4->option & WCM_OPTION_MASK_AUTH) == WCM_OPTION_AUTH_SHAREDKEY ? (u16) WM_AUTHMODE_SHARED_KEY :
                                                     (u16) WM_AUTHMODE_OPEN_SYSTEM));
            break;
        }
        switch (wmResult)
        {
        case WM_ERRCODE_OPERATING:
            break;
        case WM_ERRCODE_FIFO_ERROR:
#if WCM_DEBUG
            switch (cb->apiid)
            {
            case WM_APIID_ENABLE:
                WCMi_Printf(wcmReportText_WmSyncError, "native_fn_020126e4", wmResult);
                break;
            case WM_APIID_POWER_OFF:
                WCMi_Printf(wcmReportText_WmSyncError, "native_fn_020126a4", wmResult);
                break;
            case WM_APIID_SET_LIFETIME:
                WCMi_Printf(wcmReportText_WmSyncError, "native_fn_020141b0", wmResult);
                break;
            case WM_APIID_SET_BEACON_IND:
                WCMi_Printf(wcmReportText_WmSyncError, "native_fn_0201407c", wmResult);
                break;
            case WM_APIID_SET_WEPKEY_EX:
                WCMi_Printf(wcmReportText_WmSyncError, "native_fn_02012cb8", wmResult);
                break;
            }
#endif
            native_fn_0208a5ac(WCM_PHASE_IRREGULAR);
            native_fn_0208a550(WCM_RESULT_FAILURE, (native_data_021cfcb4->notifyId == WCM_NOTIFY_CONNECT ? &(native_data_021cfcb4->bssDesc) : 0), 0, 1711);
            break;
        case WM_ERRCODE_ILLEGAL_STATE:
            WCMi_Warning(wcmWarningText_InvalidWmState);
        default:
            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
            native_fn_0208a550(WCM_RESULT_FATAL_ERROR, (native_data_021cfcb4->notifyId == WCM_NOTIFY_CONNECT ? &(native_data_021cfcb4->bssDesc) : 0), 0, 1720);
        }
        break;
    case WM_ERRCODE_FAILED:
#if WCM_DEBUG
        switch (cb->apiid)
        {
        case WM_APIID_ENABLE:
            WCMi_Printf(wcmReportText_WmAsyncError, "native_fn_02012630", cb->errcode, cb->wlCmdID, cb->wlResult);
            break;
        case WM_APIID_DISABLE:
            WCMi_Printf(wcmReportText_WmAsyncError, "native_fn_020126a4", cb->errcode, cb->wlCmdID, cb->wlResult);
            break;
        case WM_APIID_POWER_ON:
            WCMi_Printf(wcmReportText_WmAsyncError, "native_fn_020126e4", cb->errcode, cb->wlCmdID, cb->wlResult);
            break;
        case WM_APIID_POWER_OFF:
            WCMi_Printf(wcmReportText_WmAsyncError, "native_fn_02012724", cb->errcode, cb->wlCmdID, cb->wlResult);
            break;
        case WM_APIID_SET_LIFETIME:
            WCMi_Printf(wcmReportText_WmAsyncError, "WM_SetLifeTime", cb->errcode, cb->wlCmdID, cb->wlResult);
            break;
        case WM_APIID_SET_BEACON_IND:
            WCMi_Printf(wcmReportText_WmAsyncError, "native_fn_020141b0", cb->errcode, cb->wlCmdID, cb->wlResult);
            break;
        case WM_APIID_SET_WEPKEY_EX:
            WCMi_Printf(wcmReportText_WmAsyncError, "native_fn_0201407c", cb->errcode, cb->wlCmdID, cb->wlResult);
            break;
        }
#endif
        native_fn_0208a5ac(WCM_PHASE_IRREGULAR);
        native_fn_0208a550(WCM_RESULT_FAILURE, (native_data_021cfcb4->notifyId == WCM_NOTIFY_CONNECT ? &(native_data_021cfcb4->bssDesc) : 0), 0, 1758);
        break;
    case WM_ERRCODE_ILLEGAL_STATE:
    case WM_ERRCODE_WM_DISABLE:
        WCMi_Warning(wcmWarningText_InvalidWmState);
    default:
        native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
        native_fn_0208a550(WCM_RESULT_FATAL_ERROR, (native_data_021cfcb4->notifyId == WCM_NOTIFY_CONNECT ? &(native_data_021cfcb4->bssDesc) : 0), 0, 1768);
    }
}
