#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_main_027e1b68(void *arg)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WlMaMpAckInd *pInd;
    BOOL result;
    ((void)0) ;
    pInd = (WlMaMpAckInd *)native_host_arm7_arm_037fcc74(sys->arenaId, sys->heapHandle, sizeof(WlMaMpAckInd));
    ((void) 0) ;
    pInd->header.code = (0x0100 | 0x85) ;
    pInd->header.length = 0;
    result = native_host_arm7_arm_037fc6d4(&(sys->fromWLmsgQ), (OSMessage)pInd, 0 );
    if (!result) {
        native_host_arm7_arm_027e1a08((WlCmdReq *)pInd);
        if (sys->wm7buf != ((void *)0) ) {
            WMIndCallback *cb = (WMIndCallback *)native_host_arm7_arm_038073f0();
            cb->apiid = WM_APIID_INDICATION;
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->state = WM_STATECODE_FIFO_ERROR;
            cb->reason = WM_APIID_INDICATION;
            native_host_arm7_arm_038073a4(cb);
        }
    }
}
