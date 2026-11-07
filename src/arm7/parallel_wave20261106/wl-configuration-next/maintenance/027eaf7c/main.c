#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027eaf7c(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl;
    switch (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.Mode) {
    case 1 :
        if (native_host_arm7_arm_027eae74(&pTxCtrl->Beacon)) {
            native_host_arm7_arm_027eaef4();
            native_host_arm7_arm_027f1210();
            ;
            ;
        }
        if (native_host_arm7_arm_027eae74(&pTxCtrl->Txq[2])) {
            ;
            native_host_arm7_arm_027eaf30(&pTxCtrl->Txq[2]);
        }
        break;
    case 2 :
        if (native_host_arm7_arm_027eae74(&pTxCtrl->Key[1])) {
            ;
        }
        if (native_host_arm7_arm_027eae74(&pTxCtrl->Txq[2])) {
            ;
            if (pTxCtrl->Txq[2].Busy) {
                native_host_arm7_arm_027eaef4();
            }
            native_host_arm7_arm_027f1f5c(pWork->AID);
            ;
            pWork->TxBufResCount++;
        }
        break;
    case 3 :
        break;
    }
    if (native_host_arm7_arm_027eae74(&pTxCtrl->Txq[1])) {
        ;
        native_host_arm7_arm_027eaf30(&pTxCtrl->Txq[1]);
    }
    if (native_host_arm7_arm_027eae74(&pTxCtrl->Txq[0])) {
        ;
        native_host_arm7_arm_027eaf30(&pTxCtrl->Txq[0]);
    }
    if (*(vu16 *)((0x04808000) + 0x004) == 0) {
        *(vu16 *)((0x04808000) + 0x004) = 1;
    }
}
