typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037f8714(u32, u32);
extern u32 native_utility_child_arm7_arm_037f8558(u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_wram_037f86d4(u32 *arg0) {
    u32 *var_r0;
    u32 temp_r1;

    var_r0 = arg0;
    temp_r1 = *var_r0;
    if (temp_r1 != 0) {
        native_utility_child_arm7_arm_037f8714(*native_utility_child_arm7_data_0380fff4 + 0x200, temp_r1);
        var_r0 = (u32 *) native_utility_child_arm7_arm_037f8558(2U, 0xBU);
    }
    return (u32) var_r0;
}
