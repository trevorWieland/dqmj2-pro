typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02001d79(u32);
extern u8 native_utility_child_arm9_data_020266c0[];
extern u8 native_utility_child_arm9_data_02022540[];
u32 native_utility_child_arm9_main_02001e58(void) {
    M2C_FIELD(native_utility_child_arm9_data_020266c0, u8 *, 0) = 0;
    return native_utility_child_arm9_thumb_02001d79((u32) (native_utility_child_arm9_data_02022540 + (M2C_FIELD(native_utility_child_arm9_data_020266c0, s32 *, 0xC) * 0x10)));
}
