#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027f1f5c(u16 aid)
{
    LPTXFRM_MAC pMFrm = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl.Txq[2 ].pMacFrm;
    ;
    pMFrm->MacHeader.Tx.Status = 0;
    pMFrm->MacHeader.Tx.Status2 = 0;
    pMFrm->MacHeader.Tx.rsv_RetryCount = 0;
    pMFrm->MacHeader.Tx.MPDU = 28 - 6 - 2;
    pMFrm->Dot11Header.FrameCtrl.Data = ((0x01 * 0x0004) | (0x0A * 0x0010)) ;
    pMFrm->Dot11Header.DurationID = 0xC000 | aid;
    native_host_arm7_arm_027ea108(pMFrm->Dot11Header.Adrs1, ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.BSSID, ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.MacAdrs);
}
