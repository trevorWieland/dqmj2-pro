typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200b270(void);
extern u32 native_utility_child_arm9_thumb_0200b2ec(u32);
extern u32 native_utility_child_arm9_thumb_0200b2a0(u32);
u32 native_utility_child_arm9_main_020064c4(void) {
    u32 temp_r4;

    temp_r4 = native_utility_child_arm9_thumb_0200b270();
    native_utility_child_arm9_thumb_0200b2ec(1U);
    return native_utility_child_arm9_thumb_0200b2a0(temp_r4);
}
