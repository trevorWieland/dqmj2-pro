typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02007a68(u32, u32, u32);
extern u8 native_utility_child_arm9_data_0202920c[];
u32 native_utility_child_arm9_main_02007580(u32 arg0) {
    if (native_utility_child_arm9_thumb_02007a68(M2C_FIELD(native_utility_child_arm9_data_0202920c, u32 *, 8), 0x400U, arg0) != 0) {
        return 1U;
    }
    return 0U;
}
