typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02009f84(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_0200a15c(u32);
extern u32 native_utility_child_arm9_thumb_0200a168(u32);
extern u32 native_utility_child_arm9_arm_02003934(u32, u32, u32);
extern u8 native_utility_child_arm9_data_02027c94[];
u32 native_utility_child_arm9_main_0200218c(void) {
    u32 temp_r0;
    u32 temp_r4;
    u32 temp_r5;
    u32 temp_r5_2;
    u32 temp_r6;

    temp_r4 = native_utility_child_arm9_thumb_02009f84(0U, 0x10000U, 0x10U);
    temp_r5 = native_utility_child_arm9_thumb_0200a15c(0U);
    temp_r5_2 = (native_utility_child_arm9_thumb_0200a168(0U) & ~0xF) - ((temp_r5 + 0xF) & ~0xF);
    temp_r6 = native_utility_child_arm9_thumb_02009f84(0U, temp_r5_2, 0x10U);
    M2C_FIELD(native_utility_child_arm9_data_02027c94, u32 *, 0) = native_utility_child_arm9_arm_02003934(temp_r4, 0x10000U, 0U);
    temp_r0 = native_utility_child_arm9_arm_02003934(temp_r6, temp_r5_2, 0U);
    M2C_FIELD(native_utility_child_arm9_data_02027c94, u32 *, 4) = temp_r0;
    return temp_r0;
}
