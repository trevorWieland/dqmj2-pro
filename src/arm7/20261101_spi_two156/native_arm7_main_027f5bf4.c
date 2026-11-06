#include "native_spi_types.h"
u32 native_arm7_main_027f5bf4(u32 address) {
    u16 status;
    u8 *output=(u8 *)address;
    do { status=((volatile u16 *)0x040001c0)[0]; } while(status&0x80);
    ((volatile u16 *)0x040001c0)[0]=0x8900;
    ((volatile u16 *)0x040001c2)[0]=0x9f;
    do { status=((volatile u16 *)0x040001c0)[0]; } while(status&0x80);
    ((volatile u16 *)0x040001c2)[0]=0;
    do { status=((volatile u16 *)0x040001c0)[0]; } while(status&0x80);
    output[0]=(u8)((volatile u16 *)0x040001c2)[0];
    ((volatile u16 *)0x040001c0)[0]=0x8100;
    ((volatile u16 *)0x040001c2)[0]=0;
    do { status=((volatile u16 *)0x040001c0)[0]; } while(status&0x80);
    output[1]=(u8)((volatile u16 *)0x040001c2)[0];
    return address;
}
