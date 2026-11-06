typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_data_027ffd9c[];
extern u8 native_utility_child_arm9_data_02600000[];
extern u8 native_utility_child_arm9_data_02800000[];
extern u32 native_utility_child_arm9_data_02029568[];
extern u8 native_utility_child_arm9_data_0200a2d8[];
extern u8 native_utility_child_arm9_data_027e3f80[];
extern u32 native_utility_child_arm9_data_02029560[];
u32 native_utility_child_arm9_main_0200a45c(void) {
    if (((u32) *native_utility_child_arm9_data_027ffd9c >= (u32) native_utility_child_arm9_data_02600000) && ((u32) *native_utility_child_arm9_data_027ffd9c < (u32) native_utility_child_arm9_data_02800000)) {
        *native_utility_child_arm9_data_02029568 = *native_utility_child_arm9_data_027ffd9c;
    } else {
        *native_utility_child_arm9_data_02029568 = 0;
    }
    if (*native_utility_child_arm9_data_02029568 == 0) {
        *native_utility_child_arm9_data_027ffd9c = (u32) native_utility_child_arm9_data_0200a2d8;
        M2C_FIELD(native_utility_child_arm9_data_027e3f80, u8 **, 0x5C) = native_utility_child_arm9_data_0200a2d8;
    }
    *native_utility_child_arm9_data_02029560 = 0;
    return (u32) native_utility_child_arm9_data_02029560;
}
