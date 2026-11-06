#include "context.h"
void native_main_0208ad94(void* arg)
{
    WMStartDCFCallback*     cb = (WMStartDCFCallback*)arg;
    switch (cb->errcode)
    {
    case WM_ERRCODE_SUCCESS:
        switch (cb->state)
        {
        case WM_STATECODE_DCF_START:
            if (native_data_021cfcb4->phase == WCM_PHASE_IRREGULAR)
            {
                WCMi_Printf(wcmReportText_WmDisconnected, "WM_StartDCF");
                native_fn_0208a5ac(WCM_PHASE_IDLE_TO_DCF);
                native_fn_0208a698();
            }
            else
            {
                native_fn_0208a5ac(WCM_PHASE_DCF);
                native_fn_0208a550(WCM_RESULT_SUCCESS, &(native_data_021cfcb4->bssDesc), 0, 2162);
            }
            break;
        case WM_STATECODE_DCF_IND:
            native_fn_0208b7f0((u8) (cb->recvBuf->rate_rssi >> 8));
            native_fn_020072d0(cb->recvBuf, WCM_DCF_RECV_BUF_SIZE);
            native_fn_0208b474(cb->recvBuf);
            break;
        default:
            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
            native_fn_0208a550(WCM_RESULT_FATAL_ERROR, &(native_data_021cfcb4->bssDesc), (void*)(cb->state), 2177);
        }
        break;
    case WM_ERRCODE_WM_DISABLE:
        WCMi_Warning(wcmWarningText_InvalidWmState);
    default:
        native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
        native_fn_0208a550(WCM_RESULT_FATAL_ERROR, &(native_data_021cfcb4->bssDesc), 0, 2188);
    }
}
