#include "context000.h"

#include "context001.h"

static void WmspMaMultiPollAckAlarmCallback(void *arg)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WlMaMpAckInd *pInd;
    BOOL result;
    ((void)0) ;
    pInd = (WlMaMpAckInd *)OS_AllocFromHeap(sys->arenaId, sys->heapHandle, sizeof(WlMaMpAckInd));
    ((void) 0) ;
    pInd->header.code = (0x0100 | 0x85) ;
    pInd->header.length = 0;
    result = OS_SendMessage(&(sys->fromWLmsgQ), (OSMessage)pInd, 0 );
    if (!result) {
        WmspFreeBufOfWL((WlCmdReq *)pInd);
        if (sys->wm7buf != ((void *)0) ) {
            WMIndCallback *cb = (WMIndCallback *)WMSP_GetBuffer4Callback2Wm9();
            cb->apiid = WM_APIID_INDICATION;
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->state = WM_STATECODE_FIFO_ERROR;
            cb->reason = WM_APIID_INDICATION;
            WMSP_ReturnResult2Wm9(cb);
        }
    }
}
