typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe41c(void);
extern u32 native_utility_child_arm7_arm_037fe430(u32);
extern u32 native_utility_child_arm7_arm_0380576c(void);
extern u32 native_utility_child_arm7_arm_038057c8(u32);
extern u32 native_utility_child_arm7_arm_027e273c(u32, u32);
extern u32 native_utility_child_arm7_arm_027e5938(u32, u32);
extern u8 native_utility_child_arm7_data_027f94f0[];
u32 native_utility_child_arm7_main_027e5974(void) {
    u8 sp0[512];
    u16 temp_r1;
    u32 temp_r0_3;
    void *temp_r0;
    void *temp_r0_2;
    void *temp_r4;

    temp_r4 = M2C_FIELD(native_utility_child_arm7_data_027f94f0, void **, 0x550);
    temp_r0_3 = native_utility_child_arm7_arm_037fe41c();
    if (M2C_FIELD(temp_r4, u16 *, 0) != 0xB) {
        native_utility_child_arm7_arm_037fe430(temp_r0_3);
        temp_r0_2 = (void *) native_utility_child_arm7_arm_0380576c();
        M2C_FIELD(temp_r0_2, s16 *, 0) = 0x13;
        M2C_FIELD(temp_r0_2, s16 *, 2) = 3;
        return native_utility_child_arm7_arm_038057c8((u32) temp_r0_2);
    }
    M2C_FIELD(temp_r4, s32 *, 0x10) = 0;
    M2C_FIELD(temp_r4, u16 *, 0) = 8U;
    native_utility_child_arm7_arm_037fe430(temp_r0_3);
    temp_r1 = M2C_FIELD((void *) native_utility_child_arm7_arm_027e273c((u32) &sp0, 7U), u16 *, 4);
    if (temp_r1 != 0) {
        return native_utility_child_arm7_arm_027e5938(0x104U, (u32) temp_r1);
    }
    temp_r0 = (void *) native_utility_child_arm7_arm_0380576c();
    M2C_FIELD(temp_r0, s16 *, 0) = 0x13;
    M2C_FIELD(temp_r0, s16 *, 2) = 0;
    return native_utility_child_arm7_arm_038057c8((u32) temp_r0);
}
