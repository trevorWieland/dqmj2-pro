#include "context.h"
void native_main_0208af1c(void* arg)
{
    WMCallback*     cb = (WMCallback*)arg;
    WMErrCode       wmResult = WM_ERRCODE_MAX;
    switch (cb->errcode)
    {
    case WM_ERRCODE_SUCCESS:
        native_data_021cfcb4->resetting = WCM_RESETTING_OFF;
        native_data_021cfcb4->authId = 0;
        switch (native_data_021cfcb4->phase)
        {
        case WCM_PHASE_IDLE_TO_SEARCH:
        case WCM_PHASE_SEARCH:
            native_fn_0208a5ac(WCM_PHASE_IDLE);
            native_fn_0208a550(WCM_RESULT_FAILURE, 0, 0, 2293);
            break;
        case WCM_PHASE_SEARCH_TO_IDLE:
            native_fn_0208a5ac(WCM_PHASE_IDLE);
            native_fn_0208a550(WCM_RESULT_SUCCESS, 0, 0, 2299);
            break;
        case WCM_PHASE_IDLE_TO_DCF:
            {
                u16 wlStatus = native_data_021cfcb4->wlStatusOnConnectFail;
                native_data_021cfcb4->wlStatusOnConnectFail = 0x0000;
#ifdef WCM_CAMOUFLAGE_RATESET
                if (wlStatus == WCM_CONNECT_STATUSCODE_ILLEGAL_RATESET)
                {
                    if ((native_data_021cfcb4->bssDesc.rateSet.support & WCM_CAMOUFLAGE_RATESET) != WCM_CAMOUFLAGE_RATESET)
                    {
                        WCMi_Printf(wcmReportText_SupportRateset, native_data_021cfcb4->bssDesc.ssid);
                        native_data_021cfcb4->bssDesc.rateSet.support |= WCM_CAMOUFLAGE_RATESET;
                        wmResult = native_fn_02012cb8(native_fn_0208ab60, &(native_data_021cfcb4->bssDesc), NULL,
                                                     ((native_data_021cfcb4->option & WCM_OPTION_MASK_POWER) == WCM_OPTION_POWER_ACTIVE ? FALSE : TRUE),
                                                             ((native_data_021cfcb4->option & WCM_OPTION_MASK_AUTH) == WCM_OPTION_AUTH_SHAREDKEY ?
                                                                     (u16) WM_AUTHMODE_SHARED_KEY : (u16) WM_AUTHMODE_OPEN_SYSTEM
                                                                     ));
                        switch (wmResult)
                        {
                        case WM_ERRCODE_OPERATING:
                            break;
                        case WM_ERRCODE_FIFO_ERROR:
                            native_fn_0208a5ac(WCM_PHASE_IRREGULAR);
                            native_fn_0208a550(WCM_RESULT_FAILURE, &(native_data_021cfcb4->bssDesc), (void*)wlStatus, 2332);
                            break;
                        case WM_ERRCODE_ILLEGAL_STATE:
                            WCMi_Warning(wcmWarningText_InvalidWmState);
                        default:
                            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
                            native_fn_0208a550(WCM_RESULT_FATAL_ERROR, &(native_data_021cfcb4->bssDesc), (void*)wlStatus, 2341);
                        }
                        return;
                    }
                }
#endif
                native_fn_0208a5ac(WCM_PHASE_IDLE);
                native_fn_0208a550(WCM_RESULT_FAILURE, &(native_data_021cfcb4->bssDesc), (void*)wlStatus, 2349);
            }
            break;
        case WCM_PHASE_DCF:
        case WCM_PHASE_IRREGULAR:
            native_fn_0208a5ac(WCM_PHASE_IDLE);
            native_fn_0208a550(WCM_RESULT_SUCCESS, &(native_data_021cfcb4->bssDesc), (void*)1, 2357);
            break;
        case WCM_PHASE_DCF_TO_IDLE:
            native_fn_0208a5ac(WCM_PHASE_IDLE);
            native_fn_0208a550(WCM_RESULT_SUCCESS, &(native_data_021cfcb4->bssDesc), 0, 2364);
            break;
        case WCM_PHASE_TERMINATING:
            wmResult = native_fn_02012724(native_fn_0208a730);
            switch (wmResult)
            {
            case WM_ERRCODE_OPERATING:
                break;
            case WM_ERRCODE_FIFO_ERROR:
                WCMi_Printf(wcmReportText_WmSyncError, "native_fn_020127ec", wmResult);
                native_fn_0208a5ac(WCM_PHASE_IRREGULAR);
                native_fn_0208a550(WCM_RESULT_FAILURE, 0, 0, 2378);
                break;
            case WM_ERRCODE_ILLEGAL_STATE:
                WCMi_Warning(wcmWarningText_InvalidWmState);
            default:
                native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
                native_fn_0208a550(WCM_RESULT_FATAL_ERROR, 0, 0, 2387);
            }
            break;
        default:
            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
            native_fn_0208a550(WCM_RESULT_FATAL_ERROR, 0, (void*)(native_data_021cfcb4->phase), 2393);
        }
        break;
    default:
        native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
        native_fn_0208a550(WCM_RESULT_FATAL_ERROR, 0, 0, 2400);
    }
}
