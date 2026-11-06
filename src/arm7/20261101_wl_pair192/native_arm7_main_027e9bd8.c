#include "wl_measured_views.h"
u32 native_arm7_main_027e9bd8(void)
{
    unsigned long offset = 0xe2e2;
    native_host_arm7_arm_027f4e1c(0x58,2,(u32)&offset);
    offset += 0x0202;
    if (native_host_arm7_arm_027ea584() == 20) {
        offset -= (97 + 97 * 0x100);
        if (*(volatile u16 *)0x048080bc & 2) {
            offset -= (96 + 96 * 0x100);
        }
    }
    *(volatile u16 *)0x04808140 = offset;
    return 0x04808140;
}
