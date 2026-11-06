typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fb844(void);
extern u16 native_utility_child_arm7_data_04808094[];
u32 native_utility_child_arm7_main_027ea1fc(void) {
    u32 var_r0;

    var_r0 = *native_utility_child_arm7_data_04808094 & 0x8000;
    if (var_r0 == 0) {
        var_r0 = native_utility_child_arm7_arm_037fb844();
    }
    return var_r0;
}
