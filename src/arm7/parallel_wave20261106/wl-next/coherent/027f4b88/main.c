#include "context000.h"

#include "context001.h"

#include "context002.h"

void native_host_arm7_main_027f4b88(u16 channel, LPBEACON_FRAME pFrm, LPSSID_ELEMENT pSSID)
{
    LPAP_LIST pApList = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->ApList;
    u32 i, j;
    u32 free0, free1, life1;
    if (native_host_arm7_arm_027ead5c(&pSSID->Length) > 32 ) {
        return;
    }
    free0 = 4 ;
    free1 = 4 ;
    life1 = 1024 ;
    for (i = 0; i < 4 ; i++, pApList++) {
        if (pApList->rssi != 0) {
            if (native_host_arm7_arm_027ea480(pApList->bssid, pFrm->Dot11Header.BSSID)) {
                goto write_ap_list;
            } else if (pApList->lifeTime < life1) {
                life1 = pApList->lifeTime;
                free1 = i;
            }
        } else {
            free0 = i;
        }
    }
    if (free0 != 4 ) {
        i = free0;
    } else if (free1 != 4 ) {
        i = free1;
    } else {
        return;
    }
write_ap_list:
    pApList = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->ApList[i];
    MI_CpuClear16((void *)(u32)pApList, sizeof(AP_LIST)) ;
    pApList->lifeTime = 1024 ;
    pApList->rssi = LoadLow(&pFrm->MacHeader.Rx.rsv_RSSI);
    pApList->channel = channel;
    native_host_arm7_arm_027ea0ec(pApList->bssid, pFrm->Dot11Header.BSSID);
    pApList->ssidLength = native_host_arm7_arm_027ead5c(&pSSID->Length);
    for (j = 0; j < pApList->ssidLength; j++) {
        native_host_arm7_arm_027ead30(&pApList->ssid[j], native_host_arm7_arm_027ead5c(&pSSID->SSID[j]));
    }
    pApList->beaconInterval = pFrm->Body.BeaconInterval;
    pApList->capaInfo = pFrm->Body.CapaInfo.Data;
}
