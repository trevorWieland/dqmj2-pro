#include "native_spi_types.h"
u32 native_arm7_main_027f54f0(u32 selector) {
    u16 status;
    *(volatile u16 *)0x040001c2 = (u8)selector;
    do { status = *(volatile u16 *)0x040001c0; } while (status & 0x80);
    return status;
}
