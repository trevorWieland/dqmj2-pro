typedef unsigned int u32;
extern u32 native_utility_child_arm9_fn_0200a64c(void);
extern void native_utility_child_arm9_fn_0200a660(u32);
void native_utility_child_arm9_itcm_01ff81f0(u32 channel, u32 source, u32 destination, u32 control) {
    u32 flags;
    volatile u32 *registers;
    flags = native_utility_child_arm9_fn_0200a64c();
    registers = (volatile u32 *)(0x040000b0 + channel * 12);
    registers[0] = source;
    registers[1] = destination;
    registers[2] = control;
    (void)*(volatile u32 *)0x040000b0;
    (void)*(volatile u32 *)0x040000b0;
    if (channel == 0) {
        registers[0] = 0;
        registers[1] = 0;
        registers[2] = 0x81400001;
    }
    native_utility_child_arm9_fn_0200a660(flags);
}
void native_utility_child_arm9_itcm_01ff8238(u32 channel, u32 source, u32 destination, u32 control) {
    u32 flags;
    volatile u32 *registers;
    flags = native_utility_child_arm9_fn_0200a64c();
    registers = (volatile u32 *)(0x040000b0 + channel * 12);
    registers[0] = source;
    registers[1] = destination;
    registers[2] = control;
    native_utility_child_arm9_fn_0200a660(flags);
}
