typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
u32 native_utility_child_arm7_wram_037f8aa4(u8 *value) {
    return *(volatile u32 *)(value + 4);
}
