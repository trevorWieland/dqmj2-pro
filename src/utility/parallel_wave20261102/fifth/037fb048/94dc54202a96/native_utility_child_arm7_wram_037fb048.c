#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_wram_037fb048(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl;
    u32 cnt;
    if (pTxCtrl->Mp.Busy == 0) {
        return;
    }
    if (pTxCtrl->pMpEndInd->mpKey.bitmap != pTxCtrl->Mp.pMacFrm->MacHeader.Tx.Status2) {
        native_utility_child_arm7_arm_037fac70();
    }
    cnt = LoadLow(&pTxCtrl->Mp.pMacFrm->MacHeader.Tx.rsv_RetryCount);
    if (cnt) {
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Counter.multiPoll.txMp += cnt;
    } else {
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Counter.multiPoll.txMp++;
    }
    pTxCtrl->Mp.OutCount++;
    pTxCtrl->pMpEndInd->mpKey.errBitmap = pTxCtrl->pMpEndInd->mpKey.bitmap ^ pTxCtrl->Mp.pMacFrm->MacHeader.Tx.Status2;
    pTxCtrl->RestBitmap = pTxCtrl->pMpEndInd->mpKey.bitmap;
    pTxCtrl->Mp.Busy = 0 ;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.TmpttPs) {
        native_utility_child_arm7_arm_027ea414();
    }
    native_utility_child_arm7_arm_037f8dc4(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan.TmpBuf, pTxCtrl->pMpEndInd);
}
