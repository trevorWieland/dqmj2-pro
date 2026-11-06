typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037f8870(u32, u32);
extern u32 native_utility_child_arm7_arm_027e9164(u32);
extern u32 native_utility_child_arm7_arm_027f08c8(u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027f1090(u32 arg0, s16 arg1) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r0 = native_utility_child_arm7_arm_037f8870(*native_utility_child_arm7_data_0380fff4 + 0x188, 0x36U);
    if (temp_r0 == 0) {
        native_utility_child_arm7_arm_027e9164(2U);
        return temp_r0;
    }
    M2C_FIELD(temp_r0, u16 *, 0xC) = 0xFFFF;
    temp_r4 = temp_r0 + 0x10;
    native_utility_child_arm7_arm_027f08c8(temp_r4, arg0);
    M2C_FIELD(temp_r4, s16 *, 0x2C) = arg1;
    M2C_FIELD(temp_r4, u16 *, 6) = 2U;
    M2C_FIELD(temp_r4, s16 *, 0x12) = (s16) (M2C_FIELD(temp_r4, u16 *, 6) + 0x1C);
    M2C_FIELD(temp_r4, s16 *, 0x14) = 0xA0;
    return temp_r4;
}
