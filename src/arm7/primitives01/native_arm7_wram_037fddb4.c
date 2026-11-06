typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_arm7_data_038078c8[];
u32 native_arm7_wram_037fddb4(void) {
    return *(volatile u16 *)(native_arm7_data_038078c8 + 2);
}
