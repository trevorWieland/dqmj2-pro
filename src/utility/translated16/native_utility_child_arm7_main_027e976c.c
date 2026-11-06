typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037f8558(u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
void native_utility_child_arm7_main_027e976c(void) {
    u32 temp_r4;

    temp_r4 = *native_utility_child_arm7_data_0380fff4;
    M2C_FIELD(temp_r4, s32 *, 0x3EC) = (s32) (M2C_FIELD(temp_r4, s32 *, 0x3EC) + 1);
    native_utility_child_arm7_arm_037f8558(1U, 0xAU);
    native_utility_child_arm7_arm_037f8558(2U, 0x12U);
    native_utility_child_arm7_arm_037f8558(1U, 0x11U);
    if (M2C_FIELD(temp_r4, u16 *, 0x1FC) != 0) {
        native_utility_child_arm7_arm_037f8558(2U, 0x13U);
    }
    if (M2C_FIELD(temp_r4, u16 *, 0x3F4) != 0) {
        native_utility_child_arm7_arm_037f8558(2U, 0x15U);
    }
}
