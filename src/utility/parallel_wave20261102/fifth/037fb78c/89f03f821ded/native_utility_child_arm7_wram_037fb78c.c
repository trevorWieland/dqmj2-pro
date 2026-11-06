#include "dependency000.h"

void native_utility_child_arm7_wram_037fb78c(void)
{
    u32 i;
    for (i = 4000; i > 0; i--) {
        if (*(vu16 *)((0x04808000) + 0x19C) & (0x0001 << 7) ) {
            return;
        }
    }
    ;
}
