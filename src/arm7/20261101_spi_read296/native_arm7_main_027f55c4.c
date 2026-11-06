#include "native_spi_types.h"
extern u32 native_host_arm7_arm_027f56c8(void);
u32 native_arm7_main_027f55c4(u32 address, u32 count, u8 *destination) {
    u32 result = address;
    if (count >= 1) {
        u16 parts[3] = {(u16)((address & 0xff0000) >> 16), (u16)((address & 0xff00) >> 8), (u16)(address & 255)};
        u16 status;
        u32 received;
        do { status = ((volatile u16 *)0x040001c0)[0]; } while (status & 0x80);
        ((volatile u16 *)0x040001c0)[0] = 0x8900;
        ((volatile u16 *)0x040001c2)[0] = 3;
        {
            int index = 0;
            do {
                do { status = ((volatile u16 *)0x040001c0)[0]; } while (status & 0x80);
                ((volatile u16 *)0x040001c2)[0] = (u8)parts[index];
                index++;
            } while (index < 3);
        }
        do { status = ((volatile u16 *)0x040001c0)[0]; } while (status & 0x80);
        for (received = 0; received < count - 1; received++) {
            ((volatile u16 *)0x040001c2)[0] = 0;
            do { status = ((volatile u16 *)0x040001c0)[0]; } while (status & 0x80);
            destination[received] = (u8)((volatile u16 *)0x040001c2)[0];
        }
        ((volatile u16 *)0x040001c0)[0] = 0x8100;
        native_host_arm7_arm_027f56c8();
        result = ((volatile u16 *)0x040001c2)[0];
        destination[received] = (u8)result;
    }
    return result;
}
