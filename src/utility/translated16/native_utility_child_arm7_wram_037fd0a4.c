typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fcffc(u32);
extern u32 native_utility_child_arm7_arm_037fcf90(u32, u32);
extern u32 native_utility_child_arm7_arm_037fcfa4(u32);
extern u32 native_utility_child_arm7_arm_037fcf7c(u32, u32);
extern u32 native_utility_child_arm7_data_03805b2c[];
u32 native_utility_child_arm7_wram_037fd0a4(void) {
    u32 var_r0;

    var_r0 = *native_utility_child_arm7_data_03805b2c;
    if (var_r0 == 0) {
        *native_utility_child_arm7_data_03805b2c = 1;
        native_utility_child_arm7_arm_037fcf90(1U, native_utility_child_arm7_arm_037fcffc(1U));
        native_utility_child_arm7_arm_037fcf7c(1U, native_utility_child_arm7_arm_037fcfa4(1U));
        native_utility_child_arm7_arm_037fcf90(7U, native_utility_child_arm7_arm_037fcffc(7U));
        native_utility_child_arm7_arm_037fcf7c(7U, native_utility_child_arm7_arm_037fcfa4(7U));
        native_utility_child_arm7_arm_037fcf90(8U, native_utility_child_arm7_arm_037fcffc(8U));
        var_r0 = native_utility_child_arm7_arm_037fcf7c(8U, native_utility_child_arm7_arm_037fcfa4(8U));
    }
    return var_r0;
}
