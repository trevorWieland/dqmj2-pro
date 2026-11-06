typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e7fcc(void);
extern u32 native_utility_child_arm7_arm_027e2eec(u32);
extern u32 native_utility_child_arm7_arm_027e8228(u32, u32);
extern u32 native_utility_child_arm7_arm_0380576c(void);
extern u32 native_utility_child_arm7_arm_038057c8(u32);
extern u8 native_utility_child_arm7_data_027f94f0[];
u32 native_utility_child_arm7_main_027e2e3c(void *arg0) {
    void *temp_r0;
    void *temp_r0_2;
    s16 *temp_r2;
    void *temp_r4;
    u16 sp0;
    u16 sp2;

    temp_r4 = M2C_FIELD(arg0, void **, 4);
    M2C_FIELD(native_utility_child_arm7_data_027f94f0, void **, 0x54C) = temp_r4;
    temp_r2 = M2C_FIELD(arg0, s16 **, 8);
    M2C_FIELD(native_utility_child_arm7_data_027f94f0, s16 **, 0x550) = temp_r2;
    M2C_FIELD(temp_r4, s16 **, 0) = temp_r2;
    M2C_FIELD(temp_r4, s32 *, 8) = (s32) M2C_FIELD(arg0, s32 *, 0xC);
    native_utility_child_arm7_arm_027e7fcc();
    native_utility_child_arm7_arm_027e2eec(0xFU);
    *M2C_FIELD(temp_r4, s16 **, 0) = 1;
    if (native_utility_child_arm7_arm_027e8228((u32) &sp0, (u32) &sp2) == 0) {
        temp_r0_2 = (void *) native_utility_child_arm7_arm_0380576c();
        M2C_FIELD(temp_r0_2, s16 *, 0) = 0;
        M2C_FIELD(temp_r0_2, s16 *, 2) = 1;
        M2C_FIELD(temp_r0_2, u16 *, 4) = sp0;
        M2C_FIELD(temp_r0_2, u16 *, 6) = sp2;
        return native_utility_child_arm7_arm_038057c8((u32) temp_r0_2);
    }
    *M2C_FIELD(temp_r4, s16 **, 0) = 2;
    temp_r0 = (void *) native_utility_child_arm7_arm_0380576c();
    M2C_FIELD(temp_r0, s16 *, 0) = 0;
    M2C_FIELD(temp_r0, s16 *, 2) = 0;
    return native_utility_child_arm7_arm_038057c8((u32) temp_r0);
}
