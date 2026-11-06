typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
void native_utility_child_arm7_wram_037ffa80(u8 *target, u32 value) {
    *(volatile u8 *)(target + 29) = value;
}
