typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200b204(void);
extern u32 native_utility_child_arm9_thumb_0200b1dc(void);
u32 native_utility_child_arm9_main_0200b1c0(void) {
    u32 temp_r4;

    temp_r4 = native_utility_child_arm9_thumb_0200b204();
    return (0x100 - temp_r4) - native_utility_child_arm9_thumb_0200b1dc();
}
