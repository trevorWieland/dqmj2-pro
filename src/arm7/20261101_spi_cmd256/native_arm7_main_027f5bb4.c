#include "native_spi_types.h"
u32 native_arm7_main_027f5bb4(void) {
    u16 status;
    {
        volatile u16 *control = (volatile u16 *)0x040001c0;
        do { status = control[0]; } while (status & 0x80);
        control[0] = 0x8100;
    }
    ((volatile u16 *)0x040001c2)[0] = 0xc7;
    do { status = ((volatile u16 *)0x040001c0)[0]; } while (status & 0x80);
    return status;
}
