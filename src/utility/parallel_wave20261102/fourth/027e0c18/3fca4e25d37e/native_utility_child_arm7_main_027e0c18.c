#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e0c18(WlCmdReq *req)
{
    WlMlmeAssInd *pInd = (WlMlmeAssInd *)req;
    WMStatus *status = WMSP_GetStatusStructure();
    WMStartParentCallback *callback;
    u32 *buf;
    u32 aid;
    aid = pInd->aid;
    if (aid == 0 || aid >= (15 + 1)) {
        ((void)0) ;
        return;
    }
    if (!status->pparam.entryFlag) {
        BOOL result;
        buf = native_utility_child_arm7_arm_027e0134();
        if (buf == ((void *)0) ) {
            result = 0 ;
        } else {
            buf[0] = WM_APIID_AUTO_DEAUTH;
            native_utility_child_arm7_arm_037fe814(pInd->peerMacAdrs, &buf[1], 6);
            ((void)0) ;
            result = native_utility_child_arm7_arm_037fcccc(&(WMSP_GetSystemWork()->requestQ),
                (OSMessage)buf,
                0 );
        }
        if (!result) {
            WMIndCallback *cb = (WMIndCallback *)native_utility_child_arm7_arm_0380576c();
            cb->apiid = WM_APIID_INDICATION;
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->state = WM_STATECODE_FIFO_ERROR;
            cb->reason = WM_APIID_AUTO_DEAUTH;
            native_utility_child_arm7_arm_038057c8(cb);
        }
        return;
    }
    {
        OSIntrMode e = native_utility_child_arm7_arm_037fe41c();
        status->child_bitmap |= (0x0001 << aid);
        status->mp_readyBitmap &= ~(0x0001 << aid);
        status->mp_lastRecvTick[aid] = native_utility_child_arm7_arm_037fd724() | 1;
        native_utility_child_arm7_arm_037fe814(pInd->peerMacAdrs, status->childMacAddress[aid - 1], 6 );
        (void)native_utility_child_arm7_arm_037fe430(e);
    }
    MI_CpuFill16(status->portSeqNo[aid], 0x0001, sizeof(status->portSeqNo[0]));
    callback = (WMStartParentCallback *)native_utility_child_arm7_arm_0380576c();
    callback->apiid = WM_APIID_START_PARENT;
    callback->errcode = WM_ERRCODE_SUCCESS;
    callback->state = WM_STATECODE_CONNECTED;
    native_utility_child_arm7_arm_037fe814(pInd->peerMacAdrs, callback->macAddress, 6 );
    callback->aid = (u16)aid;
    MI_CpuCopy16(&(pInd->ssid[8]), callback->ssid, 24 );
    callback->parentSize = status->mp_parentSize;
    callback->childSize = status->mp_childSize;
    native_utility_child_arm7_arm_038057c8(callback);
}
