typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_data_03809170[];
u32 native_utility_child_arm7_wram_03804a20(u32 arg0) {
    *native_utility_child_arm7_data_03809170 = arg0;
    *(s16 *)0x08001000 = (s16) arg0;
    return arg0;
}
