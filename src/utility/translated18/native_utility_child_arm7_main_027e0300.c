typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e0298(u32);
extern u8 native_utility_child_arm7_data_027f84f0[];
u32 native_utility_child_arm7_main_027e0300(void) {
    s32 var_r3;
    u32 var_r2;

    var_r2 = 0;
    var_r3 = 0;
    do {
        var_r2 += M2C_FIELD(&native_utility_child_arm7_data_027f84f0[var_r3], u8 *, 0x1554);
        var_r3 += 1;
    } while (var_r3 < 0x20);
    return native_utility_child_arm7_arm_027e0298(var_r2 >> 5);
}
