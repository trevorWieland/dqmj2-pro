#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_wram_037fa860(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl;
    u32 bTask = 0 ;
    native_utility_child_arm7_arm_027f1a9c(2 );
    native_utility_child_arm7_arm_027f1a9c(1 );
    native_utility_child_arm7_arm_027f1a9c(0 );
    if (pTxCtrl->Txq[2 ].Busy) {
        if (pTxCtrl->Txq[2 ].pMacFrm->MacHeader.Tx.Status != 0) {
            bTask = 1 ;
        } else {
            pTxCtrl->Txq[2 ].Busy = 0;
        }
    }
    if (pTxCtrl->Txq[1 ].Busy) {
        if (pTxCtrl->Txq[1 ].pMacFrm->MacHeader.Tx.Status != 0) {
            bTask = 1 ;
        } else {
            pTxCtrl->Txq[1 ].Busy = 0;
        }
    }
    if (pTxCtrl->Txq[0 ].Busy) {
        if (pTxCtrl->Txq[0 ].pMacFrm->MacHeader.Tx.Status != 0) {
            bTask = 1 ;
        } else {
            pTxCtrl->Txq[0 ].Busy = 0;
        }
    }
    if (bTask) {
        native_utility_child_arm7_arm_037f8558(0 , 14 );
    }
    native_utility_child_arm7_arm_037f8558(0 , 20 );
}
