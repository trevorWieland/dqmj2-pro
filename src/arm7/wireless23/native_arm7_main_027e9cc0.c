typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u32 native_arm7_data_0380fff4;
extern volatile u16 native_arm7_data_0480803c[];

u32 native_arm7_main_027e9cc0(u32 value) {
    *(u16 *)((u8 *)native_arm7_data_0380fff4 + 0x354) = value >> 1;
    native_arm7_data_0480803c[0] = value;
    return 0;
}
