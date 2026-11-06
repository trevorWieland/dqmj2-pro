#include "dependency000.h"
#include "dependency001.h"

BOOL native_utility_child_arm7_main_027e03b8(u16 wmApiID, u16 *buf)
{
    WMStatus *status = WMSP_GetStatusStructure();
    WlParamSetCfm *pConfirm;
    {
        WlParamSetAllReq *pReq;
        pReq = (WlParamSetAllReq *)buf;
        native_utility_child_arm7_arm_037fe814(status->MacAddress, pReq->staMacAdrs, 6 );
        pReq->retryLimit = 7 ;
        pReq->enableChannel = status->enableChannel;
        pReq->rate = status->rate;
        pReq->mode = status->mode;
        if (status->wep_flag == 0 ) {
            pReq->wepMode = 0 ;
            pReq->wepKeyId = 0;
            MI_CpuFill16(pReq->wepKey, 0x0000, 80 );
            pReq->authAlgo = 0 ;
        } else {
            u32 dma_no = WMSP_GetSystemWork()->dmaNo;
            pReq->wepMode = status->wepMode;
            pReq->wepKeyId = status->wepKeyId;
            native_utility_child_arm7_arm_037fe814(status->wepKey, pReq->wepKey, 80 );
            pReq->authAlgo = 1 ;
        }
        pReq->beaconType = 1 ;
        pReq->probeRes = 1 ;
        if (status->mode == 1 ) {
            pReq->beaconLostTh = 0;
        } else {
            pReq->beaconLostTh = 16 ;
        }
        pReq->activeZoneTime = 10 ;
        if (wmApiID == WM_APIID_START_SCAN_EX) {
            MI_CpuFill16(&(pReq->ssidMask[0]), 0x0000, 32);
        } else {
            MI_CpuFill16(&(pReq->ssidMask[0]), 0x0000, 8);
            MI_CpuFill16(&(pReq->ssidMask[8]), 0xffff, 24);
        }
        pReq->preambleType = status->preamble;
        pConfirm = native_utility_child_arm7_arm_027e26e0(pReq);
        if (pConfirm->resultCode != 0x00 ) {
            native_utility_child_arm7_arm_027e01a4(wmApiID, (0x0200 | 0x00) , pConfirm->resultCode);
            return 0 ;
        }
    }
    return 1 ;
}
#include "dependency002.h"
