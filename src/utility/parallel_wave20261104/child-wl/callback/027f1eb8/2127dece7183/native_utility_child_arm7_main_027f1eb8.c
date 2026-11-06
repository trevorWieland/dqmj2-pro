#include "context000.h"

#include "context001.h"

void native_utility_child_arm7_main_027f1eb8(LPTXFRM pFrm, u32 flag)
{
    WlCounter *pCounter = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Counter;
    LPTXFRM_MAC pMFrm = (LPTXFRM_MAC)pFrm;
    pCounter->tx.retry += LoadLow(&pMFrm->MacHeader.Tx.rsv_RetryCount);
    if ((pMFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
        pCounter->tx.success++;
        pCounter->tx.unicast++;
    } else {
        pCounter->tx.failed++;
    }
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl.Txq[2 ].Busy = 0 ;
    ;
}
