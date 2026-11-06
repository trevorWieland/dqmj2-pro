typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe5d4(u32, u32);
extern u32 native_utility_child_arm7_arm_037fe548(u32, u32);
extern u16 native_utility_child_arm7_data_03805b88[];
u32 native_utility_child_arm7_wram_037fe594(void) {
    u16 *var_r0;

    var_r0 = native_utility_child_arm7_data_03805b88;
    if (*native_utility_child_arm7_data_03805b88 == 0) {
        *native_utility_child_arm7_data_03805b88 = 1;
        var_r0 = (u16 *) native_utility_child_arm7_arm_037fe5d4(0xCU, (u32) native_utility_child_arm7_arm_037fe548);
    }
    return (u32) var_r0;
}
