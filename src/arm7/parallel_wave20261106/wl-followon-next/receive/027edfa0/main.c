#include "context000.h"

#include "context001.h"

#include "context002.h"

u32 native_host_arm7_main_027edfa0(void *pRxFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPRXFRM pFrm = (LPRXFRM)pRxFrm;
    WlMlmeBeaconRecvInd *pInd;
    u32 i;
    u8 *p1, *p2;
    pInd = (WlMlmeBeaconRecvInd *)native_host_arm7_arm_037f886c(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan.TmpBuf, sizeof(WlMlmeBeaconRecvInd) + ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.GameInfoLength);
    if ((u32)pInd == (0) ) {
        native_host_arm7_arm_027eb078(0x0001 );
        return 0 ;
    }
    pInd->header.code = (0x0000 | 0x8D) ;
    pInd->header.length = ((sizeof(WlMlmeBeaconRecvInd) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) - 1 + (pWork->GameInfoLength + 1) / 2;
    native_host_arm7_arm_027ead30(&pInd->rssi, pFrm->MacHeader.Rx.rsv_RSSI);
    native_host_arm7_arm_027ead30(&pInd->rate, pFrm->MacHeader.Rx.Service_Rate);
    native_host_arm7_arm_027ea0ec(pInd->srcMacAdrs, pFrm->Dot11Header.Adrs2);
    pInd->gameInfoLength = pWork->GameInfoLength;
    if (pInd->gameInfoLength != 0) {
        if (pWork->GameInfoAlign & 1) {
            p1 = (u8 *)((u32)pWork->GameInfoAdrs + 1);
            p2 = (u8 *)pInd->gameInfo;
            for (i = 0; i < pInd->gameInfoLength; i++) {
                native_host_arm7_arm_027ead30(p2, native_host_arm7_arm_027ead5c(p1));
                p1++;
                p2++;
            }
        } else {
            MI_CpuCopy16((void *)(u32)pWork->GameInfoAdrs, (void *) (u32)pInd->gameInfo, pInd->gameInfoLength + 1) ;
        }
    }
    native_host_arm7_arm_037f8d58(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->HeapMan.TmpBuf, pInd) ;
    return 1 ;
}
