typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200e1b8(u32);
extern u32 native_utility_child_arm9_thumb_02002abc(u32);
extern u8 native_utility_child_arm9_data_02002b55[];
u32 native_utility_child_arm9_main_02002b38(void) {
    u32 temp_r0;

    temp_r0 = native_utility_child_arm9_thumb_0200e1b8((u32) native_utility_child_arm9_data_02002b55);
    if (temp_r0 != 2) {
        native_utility_child_arm9_thumb_02002abc(temp_r0);
        return 0U;
    }
    return 1U;
}
