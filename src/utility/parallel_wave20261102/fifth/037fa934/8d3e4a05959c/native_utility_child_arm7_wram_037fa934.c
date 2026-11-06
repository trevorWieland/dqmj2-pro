#include "dependency000.h"

void native_utility_child_arm7_wram_037fa934(void *arg)
{
    u32 x, i;
    u16 seqCtrl, seqCtrl2;
    x = native_utility_child_arm7_arm_037fbc50((1UL << 24) );
    seqCtrl = *(vu16 *)((0x04808000) + 0x210) ;
    *(vu16 *)((0x04808000) + 0x244) = 0x1000;
    for (i = 100; i > 0; i--) {
        seqCtrl2 = *(vu16 *)((0x04808000) + 0x210) ;
        if (seqCtrl != seqCtrl2) {
            break;
        }
    }
    *(vu16 *)((0x04808000) + 0x244) = 0x0000;
    native_utility_child_arm7_arm_037fa3a4(0 );
    native_utility_child_arm7_arm_037fbc8c(x);
    ;
}
