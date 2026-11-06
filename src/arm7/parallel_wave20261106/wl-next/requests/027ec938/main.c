#include "context000.h"

#include "context001.h"

u16 native_host_arm7_main_027ec938(WlCmdReq *pReqt, WlCmdCfm *pCfmt)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config;
    LPMLME_MAN pMLME = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->MLME;
    WlMlmeJoinReq *pReq = (WlMlmeJoinReq *)pReqt;
    pCfmt->header.length = ((sizeof(WlMlmeJoinCfm) - sizeof(WlCmdHeader) + 1) / 2) ;
    if ((pConfig->Mode != 3 ) && (pConfig->Mode != 2 )) {
        return 0x0B ;
    }
    if (pWork->STA < 0x20 ) {
        return 0x01 ;
    }
    native_host_arm7_arm_037f9238(0x20 );
    if (pReq->bssDesc.bssid[0] & 0x0001) {
        return 0x05 ;
    }
    if (pReq->bssDesc.ssidLength == 0) {
        return 0x05 ;
    }
    if (pReq->bssDesc.ssidLength > 32 ) {
        return 0x05 ;
    }
    if (pReq->bssDesc.beaconPeriod < 10 ) {
        return 0x05 ;
    }
    if (pReq->bssDesc.beaconPeriod > 1000 ) {
        return 0x05 ;
    }
    if (pReq->bssDesc.dtimPeriod > 255 ) {
        return 0x05 ;
    }
    if (pReq->bssDesc.channel & 0xFFF0) {
        return 0x05 ;
    }
    if (native_host_arm7_arm_027ea4b0(pReq->bssDesc.channel) == 0) {
        return 0x05 ;
    }
    if (pReq->bssDesc.rateSet.basic & ~0x0FFF ) {
        return 0x05 ;
    }
    if (pReq->bssDesc.rateSet.support & ~0x0FFF ) {
        return 0x05 ;
    }
    if (pReq->bssDesc.rateSet.basic == 0) {
        return 0x05 ;
    }
    if ((pReq->bssDesc.rateSet.support | pReq->bssDesc.rateSet.basic) == 0) {
        return 0x05 ;
    }
    if (pReq->timeOut > 2000 ) {
        return 0x05 ;
    }
    if (native_host_arm7_arm_027f4d38(0 ) != 0) {
        return 0x0E ;
    }
    if (pReq->bssDesc.capaInfo & (0x01 << 5) ) {
        native_host_arm7_arm_027e929c(1 );
    } else {
        native_host_arm7_arm_027e929c(0 );
    }
    native_host_arm7_arm_027e9578(pReq->bssDesc.bssid);
    native_host_arm7_arm_027e95dc(pReq->bssDesc.ssidLength, pReq->bssDesc.ssid);
    native_host_arm7_arm_027e96ec(pReq->bssDesc.beaconPeriod);
    native_host_arm7_arm_027e990c(pReq->bssDesc.channel, 0 );
    native_host_arm7_arm_027e9b98((LPRATE_SET)&pReq->bssDesc.rateSet);
    pMLME->pReq.Join = (WlMlmeJoinReq *)pReqt;
    pMLME->pCfm.Join = (WlMlmeJoinCfm *)pCfmt;
    pMLME->State = (0x00 | 0x20) ;
    native_host_arm7_arm_037f8598(2 , 1 );
    return 0x80 ;
}
