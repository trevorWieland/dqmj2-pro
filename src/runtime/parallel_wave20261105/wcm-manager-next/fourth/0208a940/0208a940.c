#include "context.h"
void native_main_0208a940(void* arg)
{
    WMStartScanExCallback*  cb = (WMStartScanExCallback*)arg;
    WMErrCode   wmResult = WM_ERRCODE_MAX;
    switch (cb->errcode)
    {
    case WM_ERRCODE_SUCCESS:
        if (native_data_021cfcb4->phase == WCM_PHASE_IDLE_TO_SEARCH)
        {
            native_fn_0208a5ac(WCM_PHASE_SEARCH);
            native_fn_0208a550(WCM_RESULT_SUCCESS, 0, 0, 1796);
        }
        switch (native_data_021cfcb4->phase)
        {
        case WCM_PHASE_SEARCH:
            native_data_021cfcb4->notifyId = WCM_NOTIFY_FOUND_AP;
            if (cb->state == WM_STATECODE_PARENT_FOUND)
            {
                s32 i;
                native_fn_020072d0(native_data_021cfcb4->scanExParam.scanBuf, native_data_021cfcb4->scanExParam.scanBufSize);
                for (i = 0; i < cb->bssDescCount; i++)
                {
                    native_fn_0208b260(cb->bssDesc[i], cb->linkLevel[i]);
                    native_fn_0208a57c(WCM_NOTIFY_FOUND_AP, WCM_RESULT_SUCCESS, cb->bssDesc[i], (void*)cb, 1818);
                }
            }
            if ((native_data_021cfcb4->option & WCM_OPTION_MASK_ROUNDSCAN) == WCM_OPTION_ROUNDSCAN_NOTIFY)
            {
                u32 channels = native_fn_0208a66c(native_data_021cfcb4->option & WCM_OPTION_FILTER_CHANNEL);
                if (channels > 0)
                {
                    if ((native_data_021cfcb4->scanCount % channels) == 0)
                    {
                        native_fn_0208a57c(WCM_NOTIFY_SEARCH_AROUND, WCM_RESULT_SUCCESS, (void*)(native_data_021cfcb4->scanCount), 0, 1832);
                    }
                }
            }
            native_data_021cfcb4->scanExParam.channelList = (u16) ((0x0001 << native_fn_0208a508((u16) (32 - native_fn_0208a690(cb->channelList)))) >> 1);
            native_fn_020072d0(native_data_021cfcb4->scanExParam.scanBuf, native_data_021cfcb4->scanExParam.scanBufSize);
            native_data_021cfcb4->scanCount++;
            wmResult = native_fn_02012b28(native_fn_0208a940, &(native_data_021cfcb4->scanExParam));
            break;
        case WCM_PHASE_SEARCH_TO_IDLE:
            wmResult = native_fn_02012c78(native_fn_0208ab0c);
            break;
        case WCM_PHASE_TERMINATING:
            native_fn_0208a698();
            return;
        }
        switch (wmResult)
        {
        case WM_ERRCODE_OPERATING:
            break;
        case WM_ERRCODE_FIFO_ERROR:
#if WCM_DEBUG
            switch (native_data_021cfcb4->phase)
            {
            case WCM_PHASE_SEARCH:
                WCMi_Printf(wcmReportText_WmSyncError, "native_fn_02012b28", wmResult);
                break;
            case WCM_PHASE_SEARCH_TO_IDLE:
                WCMi_Printf(wcmReportText_WmSyncError, "native_fn_02012c78", wmResult);
                break;
            }
#endif
            native_fn_0208a5ac(WCM_PHASE_IRREGULAR);
            native_fn_0208a550(WCM_RESULT_FAILURE, 0, 0, 1875);
            break;
        case WM_ERRCODE_ILLEGAL_STATE:
            WCMi_Warning(wcmWarningText_InvalidWmState);
        default:
            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
            native_fn_0208a550(WCM_RESULT_FATAL_ERROR, 0, 0, 1884);
        }
        break;
    case WM_ERRCODE_FAILED:
        WCMi_Printf(wcmReportText_WmAsyncError, "native_fn_02012b28", cb->errcode, cb->wlCmdID, cb->wlResult);
        native_fn_0208a698();
        break;
    case WM_ERRCODE_ILLEGAL_STATE:
    case WM_ERRCODE_WM_DISABLE:
        WCMi_Warning(wcmWarningText_InvalidWmState);
    default:
        native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
        native_fn_0208a550(WCM_RESULT_FATAL_ERROR, 0, 0, 1901);
    }
}
