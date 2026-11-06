#include "context000.h"

#include "context001.h"

u16 native_host_arm7_main_027ec7f8(WlCmdReq *pReqt, WlCmdCfm *pCfmt)
{
    u32 i, ch;
    WlMlmeScanReq *pReq = (WlMlmeScanReq *)pReqt;
    LPMLME_MAN pMLME = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->MLME;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config;
    pMLME->Work.Scan.MaxConfirmLength = pCfmt->header.length - 3;
    pCfmt->header.length = ((sizeof(WlMlmeScanCfm) - sizeof(WlCmdHeader) + 1) / 2) - sizeof(WlBssDesc) / 2;
    if ((pConfig->Mode != 1 ) && (pConfig->Mode != 3 ) && (pConfig->Mode != 2 )) {
        return 0x0B ;
    }
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA < 0x20 ) {
        return 0x01 ;
    }
    if (pReq->ssidLength > 32 ) {
        return 0x05 ;
    }
    if (pReq->scanType > 1 ) {
        return 0x05 ;
    }
    if (native_host_arm7_arm_027ead5c(&pReq->channelList[0]) == 0) {
        return 0x05 ;
    }
    if (pReq->maxChannelTime > 1000 ) {
        return 0x05 ;
    }
    if (pReq->maxChannelTime < 10 ) {
        return 0x05 ;
    }
    if (pReq->bssidMaskCount > 16 ) {
        return 0x05 ;
    }
    for (i = 0; i < sizeof(pReq->channelList); i++) {
        ch = native_host_arm7_arm_027ead5c(&pReq->channelList[i]);
        if (ch == 0) {
            break;
        }
        if (native_host_arm7_arm_027ea4b0(ch) == 0) {
            return 0x05 ;
        }
    }
    native_host_arm7_arm_027e9578(pReq->bssid);
    native_host_arm7_arm_027e95dc(pReq->ssidLength, pReq->ssid);
    pMLME->pReq.Scan = (WlMlmeScanReq *)pReqt;
    pMLME->pCfm.Scan = (WlMlmeScanCfm *)pCfmt;
    pMLME->State = (0x00 | 0x10) ;
    native_host_arm7_arm_037f8598(2 , 0 );
    return 0x80 ;
}
