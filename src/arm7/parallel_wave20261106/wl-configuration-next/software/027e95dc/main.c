#include "context000.h"

#include "context001.h"

u16 native_host_arm7_main_027e95dc(u16 length, u8 *pSsid)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    u32 i, b = 0;
    u8 *pBuf;
    if (length > 32 ) {
        return 0x05 ;
    }
    if ((pWork->STA == 0x40 ) && (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.Mode == 1 )) {
        if (pWork->SSIDLength != length) {
            return 0x06 ;
        }
        if (pWork->Ofst.Beacon.SSID != 0) {
            b = 1;
        }
    }
    for (i = 0; i < length; i++) {
        native_host_arm7_arm_027ead30(&pWork->SSID[i], native_host_arm7_arm_027ead5c(pSsid));
        pSsid++;
    }
    for (; i < 32 ; i++) {
        native_host_arm7_arm_027ead30(&pWork->SSID[i], 0);
    }
    pWork->SSIDLength = length;
    if (b) {
        pBuf = (u8 *)((u32)((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl.Beacon.pMacFrm + 12 + 24 + 2 + (u32)pWork->Ofst.Beacon.SSID);
        for (i = 0; i < length; i++) {
            native_host_arm7_arm_027ead30(&pBuf[i], native_host_arm7_arm_027ead5c(&pWork->SSID[i]));
        }
    }
    return 0;
}

#include "context002.h"
