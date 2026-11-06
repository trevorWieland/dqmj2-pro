typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_data_02027d30[];
extern u32 native_utility_child_arm9_data_02027d28[];
extern u32 native_utility_child_arm9_data_02027d2c[];
u32 native_utility_child_arm9_main_02005400(void) {
    *native_utility_child_arm9_data_02027d30 = 0;
    *native_utility_child_arm9_data_02027d28 = 0;
    *native_utility_child_arm9_data_02027d2c = 0;
    return (u32) native_utility_child_arm9_data_02027d2c;
}
