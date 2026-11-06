#include "../20261101_main_spi276/native_spi_types.h"
u32 native_arm7_main_027f5554(u32 destination) {
    u16 status;
    {
        volatile u16 *control = (volatile u16 *)0x040001c0;
        do { status = control[0]; } while (status & 0x80);
        control[0] = 0x8900;
    }
    ((volatile u16 *)0x040001c2)[0] = 5;
    do { status = ((volatile u16 *)0x040001c0)[0]; } while (status & 0x80);
    ((volatile u16 *)0x040001c0)[0] = 0x8100;
    ((volatile u16 *)0x040001c2)[0] = 0;
    do { status = ((volatile u16 *)0x040001c0)[0]; } while (status & 0x80);
    *((u8 *)destination) = (u8)((volatile u16 *)0x040001c2)[0];
    return destination;
}
