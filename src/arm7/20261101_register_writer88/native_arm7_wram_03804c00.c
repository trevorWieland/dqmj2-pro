typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern volatile u16 native_host_arm7_data_040001c0[];
extern u32 native_host_arm7_arm_03804c58(u32);
u32 native_arm7_wram_03804c00(u32 selector, u32 value) {
    {
        u16 status;
        volatile u16 *control = native_host_arm7_data_040001c0;
        do { status = control[0]; } while (status & 0x80);
        control[0] = 0x8202;
        control[0] = 0x8802;
    }
    native_host_arm7_arm_03804c58((u8)selector);
    {
        u8 output;
        volatile u16 *control = native_host_arm7_data_040001c0;
        output = (u8)value;
        control[0] = 0x8002;
        control[1] = output;
        return output;
    }
}
