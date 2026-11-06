#include "context.h"
s32 native_main_02089da4(void* bssid, void* essid, u32 option)
{
    OSIntrMode  e = native_fn_02007ff4();
    if (native_data_021cfcb4 == NULL)
    {
        WCMi_Warning(wcmWarningText_NotInit);
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    {
        WMErrCode   wmResult;
        switch (native_data_021cfcb4->phase)
        {
        case WCM_PHASE_IDLE:
            break;
        case WCM_PHASE_IDLE_TO_SEARCH:
            native_fn_0208a3e0(bssid, essid, option);
            (void)native_fn_02008008(e);
            return WCM_RESULT_PROGRESS;
        case WCM_PHASE_SEARCH:
            native_fn_0208a3e0(bssid, essid, option);
            (void)native_fn_02008008(e);
            return WCM_RESULT_SUCCESS;
        default:
            WCMi_Warning(wcmWarningText_IllegalPhase, native_data_021cfcb4->phase);
            (void)native_fn_02008008(e);
            return WCM_RESULT_FAILURE;
        }
        native_fn_0208a3e0(bssid, essid, option);
        native_fn_020072d0(native_data_021cfcb4->scanExParam.scanBuf, native_data_021cfcb4->scanExParam.scanBufSize);
        native_data_021cfcb4->scanCount++;
        wmResult = native_fn_02012b28(native_fn_0208a940, &(native_data_021cfcb4->scanExParam));
        switch (wmResult)
        {
        case WM_ERRCODE_OPERATING:
            native_fn_0208a5ac(WCM_PHASE_IDLE_TO_SEARCH);
            native_data_021cfcb4->notifyId = WCM_NOTIFY_BEGIN_SEARCH;
            break;
        case WM_ERRCODE_FIFO_ERROR:
            WCMi_Printf(wcmReportText_WmSyncError, "native_fn_02012b28", wmResult);
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
