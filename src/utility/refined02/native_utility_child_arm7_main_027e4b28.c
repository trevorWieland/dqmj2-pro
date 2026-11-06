typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_0380576c(void);
extern u32 native_utility_child_arm7_arm_037fe814(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_038057c8(u32);
extern u8 native_utility_child_arm7_data_027f94f0[];
u32 native_utility_child_arm7_main_027e4b28(s32 arg0, s16 arg1, u32 arg2) {
    void *temp_r0;
    void *temp_r4;

    temp_r4 = M2C_FIELD(native_utility_child_arm7_data_027f94f0, void **, 0x550);
    temp_r0 = (void *) native_utility_child_arm7_arm_0380576c();
    M2C_FIELD(temp_r0, s16 *, 2) = 0;
    if (arg0 != 0) {
        M2C_FIELD(temp_r0, s16 *, 0) = 8;
        M2C_FIELD(temp_r0, s16 *, 8) = 0x1A;
        M2C_FIELD(temp_r0, u16 *, 0x12) = 0xF001;
        M2C_FIELD(temp_r0, s16 *, 0x10) = arg1;
        native_utility_child_arm7_arm_037fe814(arg2, (u32) (temp_r0 + 0xA), 6U);
        M2C_FIELD(temp_r0, u16 *, 0x2C) = (u16) M2C_FIELD(temp_r4, u16 *, 0x30);
        M2C_FIELD(temp_r0, u16 *, 0x2E) = (u16) M2C_FIELD(temp_r4, u16 *, 0x32);
    } else {
        M2C_FIELD(temp_r0, s16 *, 0) = 0xC;
        M2C_FIELD(temp_r0, s16 *, 8) = 0x1A;
        M2C_FIELD(temp_r0, u16 *, 0xC) = 0xF001;
        M2C_FIELD(temp_r0, u16 *, 0xA) = (u16) M2C_FIELD(temp_r4, u16 *, 0x188);
        native_utility_child_arm7_arm_037fe814(arg2, (u32) (temp_r0 + 0x10), 6U);
        M2C_FIELD(temp_r0, u16 *, 0x16) = (u16) M2C_FIELD(temp_r4, u16 *, 0x30);
        M2C_FIELD(temp_r0, u16 *, 0x18) = (u16) M2C_FIELD(temp_r4, u16 *, 0x32);
    }
    return native_utility_child_arm7_arm_038057c8((u32) temp_r0);
}
