#include "dependency000.h"

void native_utility_child_arm7_wram_037fb844(void)
{
    u32 x, state, b = 1 ;
    while (b) {
        x = OS_DisableIrq();
        if ((*(vu16 *)((0x04808000) + 0x19C) & ((0x0001 << 0) | (0x0001 << 1) )) != ((0x0001 << 0) | (0x0001 << 1) )) {
            state = *(vu16 *)(0x04808000 + 0x214) ;
            if ((state != 5) && (state != 7) && (state != 8)) {
                *(vu16 *)((0x04808000) + 0x028) = 0;
                b = 0 ;
            }
        }
        OS_RestoreIrq(x);
    }
}
