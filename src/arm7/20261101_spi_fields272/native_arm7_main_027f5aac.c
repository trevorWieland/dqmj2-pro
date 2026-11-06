#include "native_spi_types.h"
extern u32 native_host_arm7_arm_027f54f0(u32);
u32 native_arm7_main_027f5aac(u32 address) {
    u16 middle;
    u8 low;
    u16 high;
    u16 status;
    low = (u8)address;
    high = (u16)((address & 0xff0000) >> 16);
    middle = (u16)((address & 0xff00) >> 8);
    do { status = ((volatile u16 *)0x040001c0)[0]; } while (status & 0x80);
    ((volatile u16 *)0x040001c0)[0] = 0x8900;
    ((volatile u16 *)0x040001c2)[0] = 0xd8;
    do { status = ((volatile u16 *)0x040001c0)[0]; } while (status & 0x80);
    native_host_arm7_arm_027f54f0(high);
    native_host_arm7_arm_027f54f0(middle);
    ((volatile u16 *)0x040001c0)[0] = 0x8100;
    return native_host_arm7_arm_027f54f0(low);
}
