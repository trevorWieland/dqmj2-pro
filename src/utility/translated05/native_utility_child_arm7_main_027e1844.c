typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e0134(void);
extern u32 native_utility_child_arm7_arm_037fcccc(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_0380576c(void);
extern u32 native_utility_child_arm7_arm_038057c8(u32);
extern u8 native_utility_child_arm7_data_027f94f0[];
extern u8 native_utility_child_arm7_data_027f8578[];
u32 native_utility_child_arm7_main_027e1844(void) {
    u32 temp_r0_2;
    u32 var_r0;
    void *temp_r0;
    void *temp_r4;

    temp_r4 = M2C_FIELD(native_utility_child_arm7_data_027f94f0, void **, 0x550);
    temp_r0_2 = native_utility_child_arm7_arm_027e0134();
    if (temp_r0_2 == 0) {
        var_r0 = 0;
    } else {
        M2C_FIELD(temp_r0_2, s32 *, 0) = 0x2D;
        M2C_FIELD(temp_r0_2, s32 *, 4) = (s32) M2C_FIELD(temp_r4, u16 *, 0x68);
        var_r0 = native_utility_child_arm7_arm_037fcccc((u32) native_utility_child_arm7_data_027f8578, temp_r0_2, 0U);
    }
    if (var_r0 != 0) {
        M2C_FIELD(temp_r4, s16 *, 0x66) = 1;
        return 1U;
    }
    temp_r0 = (void *) native_utility_child_arm7_arm_0380576c();
    M2C_FIELD(temp_r0, s16 *, 0) = 0x80;
    M2C_FIELD(temp_r0, s16 *, 2) = 8;
    M2C_FIELD(temp_r0, s16 *, 4) = 0x16;
    M2C_FIELD(temp_r0, s16 *, 6) = 0x2D;
    return native_utility_child_arm7_arm_038057c8((u32) temp_r0);
}
