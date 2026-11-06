#include "dependency000.h"

void native_host_arm7_wram_037f974c(void) __attribute__((never_inline))
{
    ;
    ;
    native_host_arm7_arm_027ea1b8();
    ;
    *(vu16 *)((0x04808000) + 0x1AC) = 0xFFFF;
    *(vu16 *)((0x04808000) + 0x010) = (0x0003 << 4) ;
}
