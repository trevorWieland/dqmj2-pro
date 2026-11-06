#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_wram_037f9978(void) __attribute__((never_inline))
{
    LPTXFRM_MAC pMFrm;
    u32 i;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 3) ;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.Diversity != 0 ) {
        if ((*(vu16 *)((0x04808000) + 0x19C) & ((0x0001 << 0) || (0x0001 << 6) )) == 0) {
            *(vu16 *)(0x04808000 + 0x290) ^= 1 ;
        }
    }
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000008 ) {
        LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
        LPTX_CTRL pTxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl;
        for (i = 0; i < 3; i++) {
            if (pTxCtrl->Txq[i].Busy) {
                pMFrm = (LPTXFRM_MAC)pTxCtrl->Txq[i].pMacFrm;
                if ((pMFrm->Dot11Header.FrameCtrl.Data & 0x4000 ) && (LoadLow(&pMFrm->MacHeader.Tx.rsv_RetryCount) != 0)) {
                    u16 *pIcv = (u16 *)(((u32)&pMFrm->Dot11Header + pMFrm->MacHeader.Tx.MPDU - 8 + 1) & 0xFFFFFFFE);
                    if ((pIcv[0] == 0) && (pIcv[1] == 0)) {
                        pMFrm->MacHeader.Tx.rsv_RetryCount = 0;
                        *(vu16 *)((0x04808000) + 0x032) = 0x0000;
                        *(vu16 *)((0x04808000) + 0x032) = 0x8000;
                        pWork->WepErrCount++;
                        ;
                        ;
                        ;
                    }
                }
            }
        }
    }
    ;
}
