#include "context.h"
void native_main_0208ab60(void* arg)
{
    WMStartConnectCallback*     cb = (WMStartConnectCallback*)arg;
    WMErrCode   wmResult = WM_ERRCODE_MAX;
    switch (cb->errcode)
    {
    case WM_ERRCODE_SUCCESS:
        switch (cb->state)
        {
        case WM_STATECODE_DISCONNECTED:
        case WM_STATECODE_BEACON_LOST:
            switch (native_data_021cfcb4->phase)
            {
            case WCM_PHASE_DCF_TO_IDLE:
                native_data_021cfcb4->authId = 0;
            case WCM_PHASE_IDLE_TO_DCF:
                native_fn_0208a5ac(WCM_PHASE_IRREGULAR);
                break;
            case WCM_PHASE_DCF:
                native_data_021cfcb4->authId = 0;
                native_data_021cfcb4->notifyId = WCM_NOTIFY_DISCONNECT;
            case WCM_PHASE_IRREGULAR:
                native_fn_0208a698();
                break;
            }
            break;
#if SDK_VERSION_MAJOR > 3 || (SDK_VERSION_MAJOR == 3 && SDK_VERSION_MINOR > 0) ||         (SDK_VERSION_MAJOR == 3 && SDK_VERSION_MINOR == 0 && SDK_VERSION_RELSTEP >= 20100)
        case WM_STATECODE_DISCONNECTED_FROM_MYSELF:
            break;
#endif
        case WM_STATECODE_CONNECT_START:
            break;
        case WM_STATECODE_CONNECTED:
            if (native_data_021cfcb4->phase == WCM_PHASE_IRREGULAR)
            {
                WCMi_Printf(wcmReportText_WmDisconnected, "native_fn_02012cb8");
                native_fn_0208a5ac(WCM_PHASE_IDLE_TO_DCF);
                native_fn_0208a698();
            }
            else
            {
                if ((WCM_AID_MIN <= cb->aid) && (cb->aid <= WCM_AID_MAX))
                {
                    native_data_021cfcb4->authId = cb->aid;
                    wmResult = native_fn_02013288(native_fn_0208ad94, (WMDcfRecvBuf *) (native_data_021cfcb4->recvBuf), WCM_DCF_RECV_BUF_SIZE);
                    switch (wmResult)
                    {
                    case WM_ERRCODE_OPERATING:
                        break;
                    case WM_ERRCODE_FIFO_ERROR:
                        WCMi_Printf(wcmReportText_WmSyncError, "native_fn_02013288", wmResult);
                        native_fn_0208a5ac(WCM_PHASE_IRREGULAR);
                        native_fn_0208a550(WCM_RESULT_FAILURE, &(native_data_021cfcb4->bssDesc), 0, 2029);
                        break;
                    case WM_ERRCODE_ILLEGAL_STATE:
                        WCMi_Warning(wcmWarningText_InvalidWmState);
                    default:
                        native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
                        native_fn_0208a550(WCM_RESULT_FATAL_ERROR, &(native_data_021cfcb4->bssDesc), 0, 2038);
                    }
                }
                else
                {
                    WCMi_Printf(wcmReportText_InvalidAid, "native_fn_02012cb8");
                    native_fn_0208a698();
                }
            }
            break;
        default:
            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
            native_fn_0208a550(WCM_RESULT_FATAL_ERROR, &(native_data_021cfcb4->bssDesc), (void*)(cb->state), 2052);
        }
        break;
    case WM_ERRCODE_FAILED:
        native_data_021cfcb4->wlStatusOnConnectFail = cb->wlStatus;
    case WM_ERRCODE_NO_ENTRY:
    case WM_ERRCODE_INVALID_PARAM:
    case WM_ERRCODE_OVER_MAX_ENTRY:
        WCMi_Printf(wcmReportText_WmAsyncError, "native_fn_02012cb8", cb->errcode, cb->wlCmdID, cb->wlResult);
        native_fn_0208a5ac(WCM_PHASE_IDLE_TO_DCF);
        native_fn_0208a698();
        break;
    case WM_ERRCODE_ILLEGAL_STATE:
    case WM_ERRCODE_WM_DISABLE:
        WCMi_Warning(wcmWarningText_InvalidWmState);
    default:
        native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
        native_fn_0208a550(WCM_RESULT_FATAL_ERROR, &(native_data_021cfcb4->bssDesc), 0, 2075);
    }
}
