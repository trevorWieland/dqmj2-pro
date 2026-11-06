typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm9_data_02027cd8[];
extern u8 native_utility_child_arm9_data_02002fed[];
u32 native_utility_child_arm9_main_020027fc(void) {
    return ((u32 (*)(s32, s32)) native_utility_child_arm9_data_02002fed)(5, M2C_FIELD(native_utility_child_arm9_data_02027cd8, s32 *, 4));
}
