typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e6580(void);
extern u32 native_utility_child_arm7_arm_027e676c(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_027e63b8(void);
extern u8 native_utility_child_arm7_data_027f94f0[];
u32 native_utility_child_arm7_main_027e64c0(void) {
    void *temp_r4;

    temp_r4 = M2C_FIELD(native_utility_child_arm7_data_027f94f0, void **, 0x550);
    native_utility_child_arm7_arm_027e6580();
    if ((u32) M2C_FIELD(temp_r4, u32 *, 0xD8) >= 0x7FU) {
        M2C_FIELD(temp_r4, s32 *, 0x1C) = 0;
    }
    return native_utility_child_arm7_arm_027e676c((u32) M2C_FIELD(temp_r4, s16 *, 0x42), (u32) native_utility_child_arm7_arm_027e63b8, 4U);
}
