#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027ef4cc(void)
{
    LPTXFRM_MAC pTxFrm = (LPTXFRM_MAC)(0x04800000 + 0x4000) ;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.SigTest2) {
        pTxFrm->MacHeader.Tx.Status = 0;
        pTxFrm->MacHeader.Tx.rsv_RetryCount = 0;
        *(vu16 *)((0x04808000) + 0x0A0) |= (0x0001 << 15) ;
    } else {
        *(vu16 *)((0x04808000) + 0x0AC) = (0x0001 << 0) ;
        *(vu16 *)((0x04808000) + 0x004) = 0;
        *(vu16 *)((0x04808000) + 0x012) = (0x0001 << 1) ;
        *(vu16 *)((0x04808000) + 0x010) = 0xFFFF;
        *(vu16 *)((0x04808000) + 0x194) = 0x0000;
        *(vu16 *)((0x04808000) + 0x040) = (0x0000 << 15) ;
    }
}
