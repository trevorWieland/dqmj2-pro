typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200eed4(u32);
extern u32 native_utility_child_arm9_thumb_0200eebc(u32);
extern u32 native_utility_child_arm9_data_0202b198[];
u32 native_utility_child_arm9_main_0200c988(u32 arg0, s32 arg1) {
    switch (arg1) {
    case 9:
        native_utility_child_arm9_thumb_0200eed4((u32) (u16) *native_utility_child_arm9_data_0202b198);
        return 0U;
    case 10:
        native_utility_child_arm9_thumb_0200eebc((u32) (u16) *native_utility_child_arm9_data_0202b198);
        return 0U;
    case 1:
        return 4U;
    default:
        return 8U;
    }
}
