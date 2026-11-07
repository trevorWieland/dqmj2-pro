#include "context000.h"

void native_host_arm7_main_027ea764(void)
{
    u32 i, data, eep_adrs;
    ;
    *(vu16 *)(0x04808000 + 0x160) = (0x0000 << 14) | (0x0001 << 8) ;
    eep_adrs = (u32)(&((LPFLASH_TABLE)0x002a)->bbpInitRegs[0]) ;
    for (i = data = 0; i < 105 ; eep_adrs++, i++) {
        native_host_arm7_arm_027f4e1c(eep_adrs, 1, (u8 *)&data);
        native_host_arm7_arm_027ea5fc(i, data);
    }
    native_host_arm7_arm_027ea5fc(90, 2);
}
