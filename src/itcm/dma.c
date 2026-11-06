typedef unsigned int u32;
typedef signed int s32;
typedef unsigned char u8;
extern u32 native_fn_02007ff4(void);
extern void native_fn_02008008(u32);
void native_itcm_01ff8448(s32 channel, u32 source, u32 destination, u32 control) {
    u32 flags;
    s32 offset;
    volatile u32 *registers;
    flags = native_fn_02007ff4();
    offset = channel * 12;
    *(volatile u32 *)(offset + 0x040000b0) = source;
    registers = (volatile u32 *)(offset + 0x040000b0);
    registers[1] = destination;
    registers[2] = control;
    native_fn_02008008(flags);
}
void native_itcm_01ff8488(s32 channel, u32 source, u32 destination, u32 control) {
    u32 flags;
    s32 offset;
    volatile u32 *registers;
    flags = native_fn_02007ff4();
    offset = channel * 12;
    *(volatile u32 *)(offset + 0x040000b0) = source;
    registers = (volatile u32 *)(offset + 0x040000b0);
    registers[1] = destination;
    registers[2] = control;
    (void)*(volatile u32 *)0x040000b0;
    (void)*(volatile u32 *)0x040000b0;
    if (channel == 0) {
        registers[0] = 0;
        registers[1] = 0;
        registers[2] = 0x81400001;
    }
    native_fn_02008008(flags);
}
void native_itcm_01ff84f8(s32 channel, u32 source, u32 destination, u32 control) {
    s32 offset;
    volatile u32 *registers;
    offset = channel * 12;
    *(volatile u32 *)(offset + 0x040000b0) = source;
    registers = (volatile u32 *)(offset + 0x040000b0);
    registers[1] = destination;
    registers[2] = control;
}
void native_itcm_01ff851c(s32 channel, u32 source, u32 destination, u32 control) {
    s32 offset;
    volatile u32 *registers;
    offset = channel * 12;
    *(volatile u32 *)(offset + 0x040000b0) = source;
    registers = (volatile u32 *)(offset + 0x040000b0);
    registers[1] = destination;
    registers[2] = control;
    (void)*(volatile u32 *)0x040000b0;
    (void)*(volatile u32 *)0x040000b0;
    if (channel == 0) {
        registers[0] = 0;
        registers[1] = 0;
        registers[2] = 0x81400001;
    }
    (void)*(volatile u32 *)0x040000b0;
    (void)*(volatile u32 *)0x040000b0;
}
