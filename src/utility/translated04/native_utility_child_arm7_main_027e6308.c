typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e676c(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_027e6250(void);
extern u32 native_utility_child_arm7_arm_027e634c(void);
extern u8 native_utility_child_arm7_data_027f94f0[];
u32 native_utility_child_arm7_main_027e6308(void) {
    u32 var_r0;

    var_r0 = M2C_FIELD(M2C_FIELD(native_utility_child_arm7_data_027f94f0, void **, 0x550), u32 *, 0xC);
    if (var_r0 == 1) {
        native_utility_child_arm7_arm_027e676c(0xD1U, (u32) native_utility_child_arm7_arm_027e634c, 3U);
        var_r0 = native_utility_child_arm7_arm_027e6250();
    }
    return var_r0;
}
