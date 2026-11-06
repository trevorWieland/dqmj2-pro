#include "context000.h"

#include "context001.h"

#include "context002.h"

void native_host_arm7_main_027f3148(LPPRBREQ_FRAME pFrm)
{
    LPPRBRES_FRAME pTxFrm;
    ELEMENT_CHECKER elementCheck;
    ;
    if (native_host_arm7_arm_027f2000(pFrm->Dot11Header.SA, ((0x00 * 0x0004) | (0x05 * 0x0010)) )) {
        return;
    }
    if ((pFrm->Dot11Header.BSSID[0] & 0x0001) || (pFrm->MacHeader.Rx.Status & (0x0001 << 15) )) {
        MI_CpuClear32(&elementCheck, sizeof(elementCheck));
        elementCheck.pElement = pFrm->Body.Buf;
        elementCheck.bodyLength = pFrm->FirmHeader.Length;
        if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.BcSsidResponse == 0 ) {
            elementCheck.foundFlag = 0x0800 ;
        }
        native_host_arm7_arm_027f3c1c(&elementCheck);
        if ((elementCheck.matchFlag & 0x0001 ) == 0x0001 ) {
            pTxFrm = native_host_arm7_arm_027f1be8(pFrm->Dot11Header.SA);
            if ((u32)pTxFrm != (0) ) {
                native_host_arm7_arm_027f1088((LPTXFRM)pTxFrm);
            }
        }
    }
}

#include "context003.h"
