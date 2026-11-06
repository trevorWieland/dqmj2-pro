#include "context000.h"

#include "context001.h"

static void SetParentTbttTxq(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl;
    u32 bTask = 0 ;
    ResetTxqPri(2 );
    ResetTxqPri(1 );
    ResetTxqPri(0 );
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
        AddTask(0 , 14 );
    }
    AddTask(0 , 20 );
}
