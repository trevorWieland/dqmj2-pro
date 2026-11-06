typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
extern u32 native_utility_child_arm9_thumb_0200d5e0(void);
extern u8 native_utility_child_arm9_data_0202b814[];
u32 native_utility_child_arm9_main_0200d4f8(s32 arg0, s32 arg1, s32 arg2) {
    u32 temp_r0;

    temp_r0 = native_utility_child_arm9_arm_0200a64c();
    if (M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 0) != 0) {
        native_utility_child_arm9_arm_0200a660(temp_r0);
        return 1U;
    }
    M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 0) = 1;
    native_utility_child_arm9_arm_0200a660(temp_r0);
    M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 0x14) = 0;
    M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 0x18) = 0;
    M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 8) = arg0;
    M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 4) = arg1;
    M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 0x10) = arg2;
    if (native_utility_child_arm9_thumb_0200d5e0() != 0) {
        return 0U;
    }
    return 3U;
}
