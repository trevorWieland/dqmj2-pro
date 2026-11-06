#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_wram_037f9aa4(void) __attribute__((never_inline))
{
    LPRX_CTRL pRxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->RxCtrl;
    LPTXQ pTxq = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl.Txq;
    u32 isr;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 2) ;
    isr = *(vu16 *)((0x04808000) + 0x1A8) ;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000008 ) {
        if (isr & (0x0001 << 10) ) {
            u16 map;
            ;
            map = *(vu16 *)((0x04808000) + 0x0B0) ;
            if ((((map & (0x0001 << 0) ) == 0) || (pTxq[0].Busy == 0)) && (((map & (0x0001 << 2) ) == 0) || (pTxq[1].Busy == 0)) && (((map & (0x0001 << 3) ) == 0) || (pTxq[2].Busy == 0)) && ((*(vu16 *)((0x04808000) + 0x19C) & (0x0001 << 0) ) == 0)) {
                *(vu16 *)((0x04808000) + 0x032) = 0x0000;
                *(vu16 *)((0x04808000) + 0x032) = 0x8000;
                pRxCtrl->IcvOkCntFlag = 0;
            }
            else if (pRxCtrl->IcvOkCntFlag++ > 12) {
                ;
                pRxCtrl->IcvOkCntFlag = 0;
                *(vu16 *)((0x04808000) + 0x032) = 0x0000;
                *(vu16 *)((0x04808000) + 0x032) = 0x8000;
                ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.WepErrCount++;
                ;
            }
        }
    }
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000001 ) {
        if (isr & ((0x0001 << 5) | (0x0001 << 6) )) {
            u16 curr = *(vu16 *)((0x04808000) + 0x054) ;
            if ((curr >= (*(vu16 *)(0x04808000 + 0x052) - ((0x04800000 + 0x4000) & 0xFFFF)) / 2) || (curr < (*(vu16 *)(0x04808000 + 0x050) - ((0x04800000 + 0x4000) & 0xFFFF)) / 2)) {
                *(vu16 *)((0x04808000) + 0x056) = *(vu16 *)((0x04808000) + 0x05A) ;
                *(u16 *)((0x04808000) + 0x030) = 0x8001;
                ;
                ;
                ;
            }
            native_utility_child_arm7_arm_027e91a8();
        }
    }
}
