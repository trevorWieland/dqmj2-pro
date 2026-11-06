#include "context000.h"

#include "context001.h"

#include "context002.h"

u32 native_host_arm7_main_027f2778(LPRXFRM pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    WlMaMpAckInd *pInd;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA != 0x40 ) {
        return 1;
    }
    if ((native_host_arm7_arm_027ea480(pFrm->Dot11Header.Adrs2, pWork->BSSID) == 0) || (native_host_arm7_arm_027ea480(pFrm->Dot11Header.Adrs3, pWork->LinkAdrs) == 0)) {
        ;
        return 1;
    }
    ;
    pFrm->FirmHeader.Length = pFrm->MacHeader.Rx.MPDU - 24 - 2 - 2;
    pInd = (WlMaMpAckInd *)(void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) ;
    pInd->header.code = (0x0100 | 0x85) ;
    pInd->header.length = ((sizeof(WlRxMpAckFrame)+1)/2) ;
    pInd->ack.txKeySts |= (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->RxCtrl.TxKeyReg | ((*(vu16 *)((0x04808000) + 0x098) & 0x8000) >> 4) | ((*(vu16 *)((0x04808000) + 0x094) & 0x8000) >> 3));
    native_host_arm7_arm_037f8d58(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan.TmpBuf, pInd);
    ;
    return 0;
}
