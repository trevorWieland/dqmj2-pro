typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027ec7a4(u32);
extern u32 native_utility_child_arm7_arm_037f899c(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_027f274c(u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027efcd8(void *arg0, void *arg1) {
    void *temp_r0;

    M2C_FIELD(arg1, s16 *, 2) = 1;
    M2C_FIELD(arg0, u16 *, 0xC) = 0xFFFF;
    temp_r0 = arg0 + 0x10;
    M2C_FIELD(temp_r0, s16 *, 2) = 0;
    M2C_FIELD(temp_r0, u16 *, 0x12) = (u16) M2C_FIELD(temp_r0, u16 *, 6);
    native_utility_child_arm7_arm_027ec7a4((u32) temp_r0);
    native_utility_child_arm7_arm_037f899c(*native_utility_child_arm7_data_0380fff4 + 0x200, *native_utility_child_arm7_data_0380fff4 + 0x194, (u32) arg0);
    native_utility_child_arm7_arm_027f274c(0U);
    return 0U;
}
