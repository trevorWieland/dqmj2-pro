#include "native_register_io_types.h"
u32 native_arm7_wram_03804c58(u32 selector) {
    u16 status;
    *(volatile u16 *)0x040001c2 = (u8)selector;
    do { status = *(volatile u16 *)0x040001c0; } while (status & 0x80);
    return status;
}
