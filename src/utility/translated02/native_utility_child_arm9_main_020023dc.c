typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm9_data_02027c9c[];
u32 native_utility_child_arm9_main_020023dc(void) {
    if (*native_utility_child_arm9_data_02027c9c == 0) {
        return 1U;
    }
    return 0U;
}
