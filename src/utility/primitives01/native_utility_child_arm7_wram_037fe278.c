typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
void native_utility_child_arm7_wram_037fe278(u8 *target) {
    *(volatile u32 *)(target + 0) = 0;
    *(volatile u32 *)(target + 8) = 0;
    *(volatile u32 *)(target + 32) = 0;
}
