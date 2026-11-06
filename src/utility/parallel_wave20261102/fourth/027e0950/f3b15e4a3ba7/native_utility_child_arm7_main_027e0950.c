#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e0950(WlCmdReq *req)
{
    int i;
    WMStatus *status = WMSP_GetStatusStructure();
    WlMlmeDeAuthInd *pInd = (WlMlmeDeAuthInd *)req;
    u8 tmpMacAddress[6];
    u16 tmpAID;
    if (WM_STATE_PARENT == status->state || WM_STATE_MP_PARENT == status->state) {
        native_utility_child_arm7_arm_037fe814(pInd->peerMacAdrs, tmpMacAddress, 6 );
        tmpAID = 0;
        for (i = 0; i < 15; ++i) {
            OSIntrMode e = native_utility_child_arm7_arm_037fe41c();
            if ((status->child_bitmap & (0x0001 << (i + 1))) && status->childMacAddress[i][0] == tmpMacAddress[0] && status->childMacAddress[i][1] == tmpMacAddress[1] && status->childMacAddress[i][2] == tmpMacAddress[2] && status->childMacAddress[i][3] == tmpMacAddress[3] && status->childMacAddress[i][4] == tmpMacAddress[4] && status->childMacAddress[i][5] == tmpMacAddress[5]) {
                tmpAID = (u16)(i + 1);
                {
                    status->child_bitmap &= ~(0x0001 << tmpAID);
                    status->mp_readyBitmap &= ~(0x0001 << tmpAID);
                    status->mp_lastRecvTick[tmpAID] = 0ULL;
                }
                MI_CpuClear8(status->childMacAddress[i], 6 );
                (void)native_utility_child_arm7_arm_037fe430(e);
                break;
            }
            (void)native_utility_child_arm7_arm_037fe430(e);
        }
        if (tmpAID == 0) {
            return;
        } else {
            WMStartParentCallback *callback = (WMStartParentCallback *)native_utility_child_arm7_arm_0380576c();
            callback->apiid = WM_APIID_START_PARENT;
            callback->errcode = WM_ERRCODE_SUCCESS;
            callback->state = WM_STATECODE_DISCONNECTED;
            callback->reason = pInd->reasonCode;
            callback->aid = tmpAID;
            native_utility_child_arm7_arm_037fe814(pInd->peerMacAdrs, callback->macAddress, 6 );
            callback->parentSize = status->mp_parentSize;
            callback->childSize = status->mp_childSize;
            native_utility_child_arm7_arm_038057c8(callback);
            if (status->mp_flag == 1 ) {
                native_utility_child_arm7_arm_027e6e08((u16)(0x0001 << tmpAID));
            }
        }
    } else {
        BOOL fCleanQueue = 0 ;
        OSIntrMode e = native_utility_child_arm7_arm_037fe41c();
        if (status->child_bitmap == 0) {
            (void)native_utility_child_arm7_arm_037fe430(e);
            return;
        }
        if (status->mp_flag == 1 ) {
            status->mp_flag = 0 ;
            fCleanQueue = 1 ;
            native_utility_child_arm7_arm_027e6834();
            native_utility_child_arm7_arm_027e0238();
        }
        status->child_bitmap = 0;
        status->mp_readyBitmap = 0;
        status->ks_flag = 0 ;
        status->dcf_flag = 0 ;
        status->VSyncFlag = 0 ;
        status->wep_flag = 0 ;
        status->wepMode = 0 ;
        MI_CpuClear8(status->wepKey, 80 );
        native_utility_child_arm7_arm_027e0100();
        status->beaconIndicateFlag = 0;
        status->state = WM_STATE_CLASS1;
        (void)native_utility_child_arm7_arm_037fe430(e);
        {
            WMStartConnectCallback *callback = (WMStartConnectCallback *)native_utility_child_arm7_arm_0380576c();
            callback->apiid = WM_APIID_START_CONNECT;
            callback->errcode = WM_ERRCODE_SUCCESS;
            callback->state = WM_STATECODE_DISCONNECTED;
            callback->reason = pInd->reasonCode;
            callback->aid = status->aid;
            native_utility_child_arm7_arm_037fe814(status->parentMacAddress, callback->macAddress, 6 );
            callback->parentSize = status->mp_parentSize;
            callback->childSize = status->mp_childSize;
            native_utility_child_arm7_arm_038057c8(callback);
        }
        if (fCleanQueue) {
            native_utility_child_arm7_arm_027e6e08(0x0001);
        }
    }
}
