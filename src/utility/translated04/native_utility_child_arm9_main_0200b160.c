typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200fa74(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200b0c8(void);
extern u32 native_utility_child_arm9_thumb_0200fa48(u32, u32);
extern u32 native_utility_child_arm9_arm_0200a6bc(u32);
extern u32 native_utility_child_arm9_thumb_0200b1a1(u32, u32);
u32 native_utility_child_arm9_main_0200b160(void) {
    u32 var_r0;

    native_utility_child_arm9_thumb_0200fa74(7U, (u32) native_utility_child_arm9_thumb_0200b1a1);
    var_r0 = native_utility_child_arm9_thumb_0200b0c8();
    if (var_r0 != 0) {
        var_r0 = native_utility_child_arm9_thumb_0200fa48(7U, 1U);
        if (var_r0 == 0) {
            do {
                native_utility_child_arm9_arm_0200a6bc(0x64U);
                var_r0 = native_utility_child_arm9_thumb_0200fa48(7U, 1U);
            } while (var_r0 == 0);
        }
    }
    return var_r0;
}
