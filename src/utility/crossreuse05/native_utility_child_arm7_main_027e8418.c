typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_0380576c(void);
extern u32 native_utility_child_arm7_arm_038057c8(u32);
extern u32 native_utility_child_arm7_arm_027e8228(u32, u32);
extern u32 native_utility_child_arm7_data_027f94f0;
u32 native_utility_child_arm7_main_027e8418(void) {
    u16 sp2;
    u16 sp0;
    u16 *temp_r4;
    void *temp_r0;
    void *temp_r0_2;
    void *temp_r0_3;

    temp_r4 = M2C_FIELD(&native_utility_child_arm7_data_027f94f0, u16 **, 0x550);
    if (*temp_r4 != 1) {
        temp_r0_3 = (void *) native_utility_child_arm7_arm_0380576c();
        M2C_FIELD(temp_r0_3, s16 *, 0) = 5;
        M2C_FIELD(temp_r0_3, s16 *, 2) = 3;
        return native_utility_child_arm7_arm_038057c8((u32) temp_r0_3);
    }
    if (native_utility_child_arm7_arm_027e8228((u32) &sp2, (u32) &sp0) == 0) {
        temp_r0_2 = (void *) native_utility_child_arm7_arm_0380576c();
        M2C_FIELD(temp_r0_2, s16 *, 0) = 5;
        M2C_FIELD(temp_r0_2, s16 *, 2) = 1;
        M2C_FIELD(temp_r0_2, u16 *, 4) = sp2;
        M2C_FIELD(temp_r0_2, u16 *, 6) = sp0;
        return native_utility_child_arm7_arm_038057c8((u32) temp_r0_2);
    }
    *temp_r4 = 2;
    temp_r0 = (void *) native_utility_child_arm7_arm_0380576c();
    M2C_FIELD(temp_r0, s16 *, 0) = 5;
    M2C_FIELD(temp_r0, s16 *, 2) = 0;
    return native_utility_child_arm7_arm_038057c8((u32) temp_r0);
}
