#include "native_register_io_types.h"
u32 native_arm7_wram_03804c7c(u32 selector) {
    {
        u16 status;
        volatile u16 *control = ((volatile u16 *)0x040001c0);
        do { status = control[0]; } while (status & 0x80);
        control[0] = 0x8202;
        control[0] = 0x8802;
    }
    native_host_arm7_arm_03804c58((u8)(selector | 0x80));
    {
        volatile u16 *control = ((volatile u16 *)0x040001c0);
        u16 status;
        control[0] = 0x8002;
        control[1] = 0;
        do { status = control[0]; } while (status & 0x80);
    }
    return (u8)((volatile u16 *)0x040001c2)[0];
}
