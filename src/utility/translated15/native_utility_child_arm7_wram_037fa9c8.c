typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027ebc2c(u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_wram_037fa9c8(void) {
    s32 temp_r4;

    temp_r4 = *native_utility_child_arm7_data_0380fff4 + 0x42C;
    if (native_utility_child_arm7_arm_027ebc2c(temp_r4 + 0x50) != 0) {
        return 1U;
    }
    if (native_utility_child_arm7_arm_027ebc2c(temp_r4 + 0x64) != 0) {
        return 1U;
    }
    return 0U;
}
