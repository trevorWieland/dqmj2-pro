typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fdcd0(void);
extern u32 native_utility_child_arm7_arm_037fdcc0(u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027e98d8(void) {
    u32 temp_r4;

    temp_r4 = *native_utility_child_arm7_data_0380fff4;
    if (native_utility_child_arm7_arm_037fdcd0() == 0) {
        M2C_FIELD(temp_r4, u16 *, 0x33E) = (u16) (M2C_FIELD(temp_r4, u16 *, 0x33E) | 0x40);
        return temp_r4 + 0x300;
    }
    native_utility_child_arm7_arm_037fdcc0(temp_r4 + 0x608);
    native_utility_child_arm7_arm_037fdcc0(temp_r4 + 0x634);
    return native_utility_child_arm7_arm_037fdcc0(temp_r4 + 0x660);
}
