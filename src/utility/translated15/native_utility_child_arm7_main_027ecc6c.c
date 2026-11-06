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
extern u32 native_utility_child_arm7_arm_037f8dc4(u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027ecc6c(void) {
    u32 temp_r0;

    temp_r0 = native_utility_child_arm7_arm_037f8870(*native_utility_child_arm7_data_0380fff4 + 0x188, 0x10U);
    if (temp_r0 == 0) {
        native_utility_child_arm7_arm_027e9164(1U);
        return 0U;
    }
    M2C_FIELD(temp_r0, s16 *, 0xC) = 0x8C;
    M2C_FIELD(temp_r0, s16 *, 0xE) = 0;
    native_utility_child_arm7_arm_037f8dc4(*native_utility_child_arm7_data_0380fff4 + 0x188, temp_r0);
    return 1U;
}
