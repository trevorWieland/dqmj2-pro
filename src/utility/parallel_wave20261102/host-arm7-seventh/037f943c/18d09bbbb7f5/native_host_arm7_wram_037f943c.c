#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_wram_037f943c(void) __attribute__((never_inline))
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config;
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl;
    u8 *p;
    u32 txq, i, vtsf;
    u32 bWakeUp;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 14) ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    switch (pWork->Mode) {
    case 1 :
        p = (u8 *)((u32)pTxCtrl->Beacon.pMacFrm->Body + pWork->Ofst.Beacon.GameInfo + 2 + 3 + 1 + 2);
        vtsf = *(vu16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) ;
        native_host_arm7_arm_027ead30(p++, vtsf & 0x00FF);
        native_host_arm7_arm_027ead30(p, vtsf >> 8);
        if (pWork->PowerMgtMode == 1 ) {
            *(vu16 *)((0x04808000) + 0x134) = (u32)pConfig->ActiveZone + *(vu16 *)((0x04808000) + 0x134) + 1;
        }
        { ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->CamMan.PowerState = (~((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->CamMan.PowerMgtMode) | ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->CamMan.NotClass3; } ;
        txq = *(vu16 *)((0x04808000) + 0x0B6) ;
        if ((txq & ((0x0001 << 4) | (0x0001 << 3) )) || ((txq & ((0x0001 << 2) | (0x0001 << 1) )) == (0x0001 << 1) )) {
            pTxCtrl->Flag &= ~0x0002 ;
            native_host_arm7_arm_037fa598();
        } else {
            pTxCtrl->Flag |= 0x0002 ;
        }
        break;
    case 2 :
        if (pWork->bSynchro) {
            *(vu16 *)((0x04808000) + 0x134) = (u32)pConfig->ActiveZone + *(vu16 *)((0x04808000) + 0x134) + 1;
        } else {
            *(vu16 *)((0x04808000) + 0x134) = 0xFFFF;
        }
        if (pWork->bFirstTbtt == 2) {
            native_host_arm7_arm_027e9cc0((0x0001 << 1) );
        }
    case 3 :
        if (pWork->STA != 0x40 ) {
            bWakeUp = 1 ;
        } else {
            bWakeUp = 0 ;
            if (pWork->CurrListenInterval == 1) {
                bWakeUp = 1 ;
            }
            if (pWork->RxDtims) {
                if ((pWork->DTIMCount == 1) || ((pWork->DTIMCount == 0) && (pWork->DTIMPeriod == 1))) {
                    bWakeUp = 1 ;
                }
            }
        }
        if (bWakeUp) {
            ;
            *(vu16 *)((0x04808000) + 0x038) |= (0x0001 << 0) ;
            ;
        } else {
            ;
            *(vu16 *)((0x04808000) + 0x038) &= ~(0x0001 << 0) ;
            ;
        }
        if (*(vu16 *)((0x04808000) + 0x118) > 10) {
            *(vu16 *)((0x04808000) + 0x048) = 0;
        }
        if (--pWork->CurrListenInterval == 0) {
            pWork->CurrListenInterval = pWork->ListenInterval;
        }
        if (pWork->DTIMCount-- == 0) {
            pWork->DTIMCount = pWork->DTIMPeriod - 1;
        }
        for (i = 0; i < 2; i++) {
            LPTXQ pTxq = &pTxCtrl->Txq[i];
            if (pTxq->Busy && (pTxq->pFrm->MacHeader.Tx.Status == 0)) {
                if (native_host_arm7_arm_027f0288(pTxq->pFrm)) {
                    native_host_arm7_arm_027f0ce0(i);
                    ;
                    pTxq->pMacFrm->MacHeader.Tx.Status = 2;
                    native_host_arm7_arm_037f8598(0 , 14 );
                    pTxCtrl->TimeOutFrm++;
                }
            }
        }
        *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 3) | (0x0001 << 2) | (0x0001 << 0) ;
        break;
    }
    ;
    ;
}
#include "dependency002.h"
