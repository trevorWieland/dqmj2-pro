typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
void native_utility_child_arm7_wram_037fc140(u8 *target, u32 value) {
    *(volatile u32 *)(target + 152) = value;
}
