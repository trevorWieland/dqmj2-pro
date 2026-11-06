#include "context.h"
DWCInetResult native_main_0209ad08 (void)
{
    int state;
    DWCInetResult result = DWC_CONNECTINET_STATE_NOT_INITIALIZED;
    if (stpInetCntl == NULL) {
        return (result);
    }
    switch (stpInetCntl->processWDSstate) {
    case DWC_WDS_STATE_IDLE:
        break;
    case DWC_WDS_STATE_PROCESS:
        return DWC_CONNECTINET_STATE_OPERATING;
    case DWC_WDS_STATE_COMPLETED:
        return DWC_CONNECTINET_STATE_OPERATING;
    case DWC_WDS_STATE_FAILED:
        native_fn_0209ac5c();
        native_fn_0209a9f8(DWC_ERROR_AC_ANY, stateOld);
        result = DWC_CONNECTINET_STATE_ERROR;
        stpInetCntl->state = result;
        stpInetCntl->processWDSstate = DWC_WDS_STATE_ERROR;
        return result;
    case DWC_WDS_STATE_ERROR:
        result = DWC_CONNECTINET_STATE_ERROR;
        return result;
    case 5:
        return 5;
    default:
        break;
    }
    result = (DWCInetResult)stpInetCntl->state;
    if (result == DWC_CONNECTINET_STATE_IDLE) {
        return (result);
    }
    state = native_fn_02094420();
    if (state == DWC_AC_STATE_COMPLETE) {
        result = DWC_CONNECTINET_STATE_CONNECTED;
        stpInetCntl->state = result;
        stpInetCntl->online = TRUE;
        stpInetCntl->wontExecuteWDS = TRUE;
    } else if (state < 0) {
        if (state >= -10) {
            stpInetCntl->wontExecuteWDS = TRUE;
            native_fn_0209a9f8(DWC_ERROR_FATAL, -50199);
            result = DWC_CONNECTINET_STATE_FATAL_ERROR;
            stpInetCntl->state = result;
        } else if (!stpInetCntl->wontExecuteWDS) {
            DWCInetControl * stepInetCntlTemp = stpInetCntl;
            u16 dmaNoTemp = stpInetCntl->dmaNo;
            u32 ssl_priority_Temp = native_fn_02090b54();
            stateOld = state;
            native_fn_0209ae18();
            native_fn_0209ab18(stepInetCntlTemp, dmaNoTemp, DWC_CONNECTINET_POWERMODE_ACTIVE, (u16)ssl_priority_Temp);
            native_fn_02096900(&(stpInetCntl->nspotInfo),1);
            stpInetCntl->processWDSstate = DWC_WDS_STATE_PROCESS;
            result = DWC_CONNECTINET_STATE_OPERATING;
            stpInetCntl->ac_state = 0;
        } else {
            if (stateOld < state) {
                state = stateOld;
            }
            native_fn_0209a9f8(DWC_ERROR_AC_ANY, state);
            result = DWC_CONNECTINET_STATE_ERROR;
            stpInetCntl->state = result;
        }
    } else {
        result = DWC_CONNECTINET_STATE_OPERATING;
    }
    return result;
}
