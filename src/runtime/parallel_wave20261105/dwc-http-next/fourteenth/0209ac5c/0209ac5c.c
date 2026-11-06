#include "context.h"
void native_main_0209ac5c (void)
{
    if (stpInetCntl == NULL) {
        return;
    }
    switch (stpInetCntl->processWDSstate) {
    case DWC_WDS_STATE_IDLE:
        break;
    case DWC_WDS_STATE_PROCESS:
        stpInetCntl->ac_state = 0;
        stpInetCntl->processWDSstate = native_fn_02096948();
        return;
    case DWC_WDS_STATE_COMPLETED:
        native_fn_02096b7c();
        native_fn_0209abec(
            stpInetCntl->nspotInfo.ssid,
            stpInetCntl->nspotInfo.wep,
            stpInetCntl->nspotInfo.wepMode,
            stpInetCntl->nspotInfo.apnum,
            DWC_AC_AP_TYPE_NINTENDOSPOT
        );
        stpInetCntl->processWDSstate = DWC_WDS_STATE_IDLE;
        return;
    case DWC_WDS_STATE_FAILED:
        native_fn_02096b7c();
        stpInetCntl->ac_state = -1;
        stpInetCntl->wontExecuteWDS = TRUE;
        return;
    case DWC_WDS_STATE_ERROR:
    case 5:
        return;
    default:
        break;
    }
    if (stpInetCntl->state == DWC_CONNECTINET_STATE_OPERATING) {
        stpInetCntl->ac_state = native_fn_02094398();
    } else if (stpInetCntl->state == DWC_CONNECTINET_STATE_CONNECTED) {
        if (stpInetCntl->online) {
            if (native_fn_0208a268() != WCM_PHASE_DCF) {
                stpInetCntl->online = FALSE;
                stpInetCntl->state = DWC_CONNECTINET_STATE_DISCONNECTED;
            }
        }
    }
}
