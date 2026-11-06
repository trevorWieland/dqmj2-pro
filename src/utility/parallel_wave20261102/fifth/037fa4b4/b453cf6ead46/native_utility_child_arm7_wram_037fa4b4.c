#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_wram_037fa4b4(void) __attribute__((never_inline))
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl;
    u32 i, cnt;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 7) ;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000020 ) {
        u16 sts = *(vu16 *)(0x04808000 + 0x214) & 0x00FF;
        u16 adr = *(vu16 *)((0x04808000) + 0x268) ;
        if (((sts >= 3) && (sts <= 5)) && ((adr >= ((u32)pTxCtrl->Key[0].pMacFrm / 2 & 0x0FFF)) && (adr <= ((u32)pTxCtrl->Txq[2].pMacFrm / 2 & 0x0FFF)))) {
            ;
            *(vu16 *)((0x04808000) + 0x244) |= 0x0080;
            *(vu16 *)((0x04808000) + 0x244) &= ~0x0080;
            ;
        }
    }
    if (*(vu16 *)((0x04808000) + 0x000) != 0x1440) {
        if ((*(vu16 *)((0x04808000) + 0x19C) & ((0x0001 << 6) | (0x0001 << 1) )) == ((0x0001 << 6) | (0x0001 << 1) )) {
            cnt = *(vu16 *)((0x04808000) + 0x2B8) ;
            if (cnt != 0) {
                i = 0;
                while (cnt == *(vu16 *)((0x04808000) + 0x2B8) ) {
                    if (i++ > 1000) {
                        ;
                        native_utility_child_arm7_arm_027e9164(0x0040 );
                        break;
                    }
                }
            }
        }
    }
    ;
}
