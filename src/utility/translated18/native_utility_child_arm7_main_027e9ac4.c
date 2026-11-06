typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027f5a70(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_027e9c78(u32, u32);
extern u16 native_utility_child_arm7_data_04808160[];
u32 native_utility_child_arm7_main_027e9ac4(void) {
    u32 var_r7;
    u32 var_r6;
    u32 sp0;

    *native_utility_child_arm7_data_04808160 = 0x100;
    var_r6 = 0x64;
    var_r7 = 0;
    sp0 = 0;
    do {
        native_utility_child_arm7_arm_027f5a70(var_r6, 1U, (u32) &sp0);
        native_utility_child_arm7_arm_027e9c78(var_r7, sp0);
        var_r6 += 1;
        var_r7 += 1;
    } while (var_r7 < 0x69U);
    return native_utility_child_arm7_arm_027e9c78(0x5AU, 2U);
}
