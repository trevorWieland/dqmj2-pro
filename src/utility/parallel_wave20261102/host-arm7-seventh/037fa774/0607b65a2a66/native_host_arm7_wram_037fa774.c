#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_wram_037fa774(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl;
    LPTXQ pTxq;
    s32 i;
    for (i = 2; i >= 0; i--) {
        pTxq = (LPTXQ)&pTxCtrl->Txq[i];
        if (((*(vu16 *)(((0x04808000) + 0x0A0) + i * 4) & (0x0001 << 15) ) == 0) && (pTxq->Busy)) {
            if (pTxq->pFrm != 0 ) {
                pTxq->pFrm->MacHeader.Tx.Status = pTxq->pMacFrm->MacHeader.Tx.Status;
                pTxq->pFrm->Dot11Header.FrameCtrl.Data = pTxq->pMacFrm->Dot11Header.FrameCtrl.Data;
                if (pTxq->pMacFrm->Dot11Header.FrameCtrl.Data & 0x4000 ) {
                    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000008 ) {
                        u16 *pIcv = (u16 *)(((u32)&pTxq->pMacFrm->Dot11Header + pTxq->pMacFrm->MacHeader.Tx.MPDU - 8 + 1) & 0xFFFFFFFE);
                        if ((pIcv[0] == 0) && (pIcv[1] == 0)) {
                            ;
                            *(vu16 *)((0x04808000) + 0x032) = 0x0000;
                            *(vu16 *)((0x04808000) + 0x032) = 0x8000;
                            pWork->WepErrCount++;
                            if (native_host_arm7_arm_027f0288(pTxq->pFrm)) {
                                pTxq->pFrm->MacHeader.Tx.Status = 2;
                                ;
                                pTxq->OutCount++;
                                pTxCtrl->TimeOutFrm++;
                                (*pTxq->pEndFunc)(pTxq->pFrm, 1);
                            } else {
                                pTxq->pFrm->MacHeader.Tx.rsv_RetryCount = 0;
                                *(vu16 *)(((0x04808000) + 0x0A0) + i * 4) |= (0x0001 << 15) ;
                            }
                            ;
                            ;
                            continue;
                        }
                    }
                    pTxq->pFrm->MacHeader.Tx.rsv_RetryCount += LoadLow(&pTxq->pMacFrm->MacHeader.Tx.rsv_RetryCount);
                } else {
                    pTxq->pFrm->MacHeader.Tx.rsv_RetryCount = LoadLow(&pTxq->pMacFrm->MacHeader.Tx.rsv_RetryCount);
                }
                pTxq->OutCount++;
                (*pTxq->pEndFunc)(pTxq->pFrm, 2);
            } else {
                pTxq->OutCount++;
                (*pTxq->pEndFunc)((LPTXFRM)pTxq->pMacFrm, 3);
            }
            ;
            ;
        }
    }
}
