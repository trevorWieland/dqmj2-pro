#include "native_spi_types.h"
u32 native_arm7_main_027f56c8(void) {
    u16 status;
    ((volatile u16 *)0x040001c2)[0] = 0;
    do { status = ((volatile u16 *)0x040001c0)[0]; } while (status & 0x80);
    return status;
}
