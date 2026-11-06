#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e1344(void *arg)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WlMaMpAckInd *pInd;
    BOOL result;
    ((void)0) ;
    pInd = (WlMaMpAckInd *)native_utility_child_arm7_arm_037fd4f8(sys->arenaId, sys->heapHandle, sizeof(WlMaMpAckInd));
    ((void) 0) ;
    pInd->header.code = (0x0100 | 0x85) ;
    pInd->header.length = 0;
    result = native_utility_child_arm7_arm_037fcccc(&(sys->fromWLmsgQ), (OSMessage)pInd, 0 );
    if (!result) {
        native_utility_child_arm7_arm_027e1e2c((WlCmdReq *)pInd);
        if (sys->wm7buf != ((void *)0) ) {
            WMIndCallback *cb = (WMIndCallback *)native_utility_child_arm7_arm_0380576c();
            cb->apiid = WM_APIID_INDICATION;
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->state = WM_STATECODE_FIFO_ERROR;
            cb->reason = WM_APIID_INDICATION;
            native_utility_child_arm7_arm_038057c8(cb);
        }
    }
}
