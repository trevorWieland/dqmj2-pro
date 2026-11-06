typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fbc50(u32);
extern u32 native_utility_child_arm7_arm_037fbc8c(u32);
extern u32 native_utility_child_arm7_arm_037f8558(u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027e9164(s32 arg0) {
    u32 temp_r0;

    temp_r0 = native_utility_child_arm7_arm_037fbc50(0x01000000U);
    M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x3F4) = (u16) (M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x3F4) | arg0);
    native_utility_child_arm7_arm_037fbc8c(temp_r0);
    return native_utility_child_arm7_arm_037f8558(2U, 0x15U);
}
