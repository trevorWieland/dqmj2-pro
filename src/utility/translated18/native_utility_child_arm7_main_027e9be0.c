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
extern u32 native_utility_child_arm7_arm_027e93d4(u32, u32);
u32 native_utility_child_arm7_main_027e9be0(void) {
    u32 var_r8;
    u32 var_r7;
    u32 var_r6;
    u32 temp_r0;
    s32 sp0;

    var_r8 = 0x64;
    var_r6 = 0;
    sp0 = 0;
    var_r7 = 0;
    do {
        native_utility_child_arm7_arm_027f5a70(var_r8, 1U, (u32) &sp0);
        if (var_r7 == 1) {
            sp0 &= 0x80;
        }
        temp_r0 = native_utility_child_arm7_arm_027e93d4((u32) (u8) sp0, var_r6);
        var_r6 = temp_r0;
        var_r8 += 1;
        var_r7 += 1;
    } while (var_r7 < 0x69U);
    return temp_r0;
}
