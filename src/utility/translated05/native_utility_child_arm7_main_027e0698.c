typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fcccc(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_037fcc2c(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_0380576c(void);
extern u32 native_utility_child_arm7_arm_038057c8(u32);
extern u32 native_utility_child_arm7_arm_027e0718(void);
extern u32 native_utility_child_arm7_arm_037fe5e0(void);
extern u8 native_utility_child_arm7_data_027f84f0[];
extern u8 native_utility_child_arm7_data_027f8548[];
u32 native_utility_child_arm7_main_027e0698(u32 arg0) {
    void *sp0;
    void *temp_r0;

    native_utility_child_arm7_arm_037fcccc((u32) native_utility_child_arm7_data_027f84f0, arg0, 1U);
    native_utility_child_arm7_arm_037fcc2c((u32) native_utility_child_arm7_data_027f8548, (u32) &sp0, 1U);
    if (M2C_FIELD((sp0 + (M2C_FIELD(sp0, u16 *, 0xE) * 2)), u16 *, 0x14) == 0xE) {
        temp_r0 = (void *) native_utility_child_arm7_arm_0380576c();
        M2C_FIELD(temp_r0, s16 *, 0) = 0x80;
        M2C_FIELD(temp_r0, s16 *, 2) = 0x13;
        M2C_FIELD(temp_r0, s16 *, 4) = 0x18;
        native_utility_child_arm7_arm_038057c8((u32) temp_r0);
        native_utility_child_arm7_arm_027e0718();
        native_utility_child_arm7_arm_037fe5e0();
    }
    return (u32) sp0;
}
