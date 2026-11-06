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
extern u32 native_utility_child_arm7_arm_027e6834(void);
extern u32 native_utility_child_arm7_arm_027e0238(void);
extern u32 native_utility_child_arm7_arm_037fe780(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_027e0100(void);
extern u32 native_utility_child_arm7_arm_037fe430(u32);
extern u32 native_utility_child_arm7_arm_027e6e08(u32);
extern u32 native_utility_child_arm7_arm_037fe6d4(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_027e08f0(void);
extern u32 native_utility_child_arm7_arm_037fcf10(u32);
extern u32 native_utility_child_arm7_arm_027e6848(void);
extern u8 native_utility_child_arm7_data_027f94f0[];
u32 native_utility_child_arm7_main_027e7fcc(void) {
    s32 temp_r7;
    s32 var_r6;
    u32 temp_r5;
    void *temp_r4;
    s32 var_r2;

    temp_r7 = M2C_FIELD(native_utility_child_arm7_data_027f94f0, s32 *, 0x54C);
    temp_r4 = M2C_FIELD(native_utility_child_arm7_data_027f94f0, void **, 0x550);
    var_r6 = 0;
    temp_r5 = native_utility_child_arm7_arm_037fe41c();
    if (M2C_FIELD(temp_r4, s32 *, 0xC) == 1) {
        M2C_FIELD(temp_r4, s32 *, 0xC) = 0;
        var_r6 = 1;
        native_utility_child_arm7_arm_027e6834();
        native_utility_child_arm7_arm_027e0238();
    }
    M2C_FIELD(temp_r4, s16 *, 0x182) = 0;
    M2C_FIELD(temp_r4, s16 *, 0x86) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x14) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x10) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x1C) = 0;
    M2C_FIELD(temp_r4, s16 *, 0xCE) = 0;
    M2C_FIELD(temp_r4, s16 *, 0xC2) = 0;
    M2C_FIELD(temp_r4, s16 *, 0x58) = 1;
    M2C_FIELD(temp_r4, s16 *, 0x5A) = 1;
    M2C_FIELD(temp_r4, s16 *, 0x5C) = 6;
    M2C_FIELD(temp_r4, s16 *, 0x98) = 0;
    M2C_FIELD(temp_r4, s16 *, 0x92) = 0;
    M2C_FIELD(temp_r4, s16 *, 0x94) = 0;
    M2C_FIELD(temp_r4, s16 *, 0x9A) = 0;
    M2C_FIELD(temp_r4, s16 *, 0x9C) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x198) = 0;
    M2C_FIELD(temp_r4, s16 *, 0x196) = 0;
    native_utility_child_arm7_arm_037fe780((u32) (temp_r4 + 0x19C), 0U, 0x50U);
    native_utility_child_arm7_arm_027e0100();
    M2C_FIELD(temp_r4, s16 *, 0x40) = 0x104;
    M2C_FIELD(temp_r4, s16 *, 0x42) = 0xF0;
    M2C_FIELD(temp_r4, s16 *, 0x44) = 0x3E8;
    M2C_FIELD(temp_r4, s16 *, 0x46) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x48) = 0x20B;
    M2C_FIELD(temp_r4, s32 *, 0x4C) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x50) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x54) = 0;
    M2C_FIELD(temp_r4, s16 *, 0xC6) = 0;
    M2C_FIELD(temp_r4, s16 *, 0x1EE) = 1;
    native_utility_child_arm7_arm_037fe430(temp_r5);
    if (var_r6 != 0) {
        native_utility_child_arm7_arm_027e6e08(0xFFFFU);
    }
    var_r2 = 0;
    do {
        M2C_FIELD((temp_r7 + (var_r2 * 0x10)), s32 *, 0xD0) = 0x8000;
        var_r2 += 1;
    } while (var_r2 < 0x20);
    native_utility_child_arm7_arm_037fe6d4(1U, (u32) (temp_r4 + 0x1F8), 0x100U);
    native_utility_child_arm7_arm_027e08f0();
    native_utility_child_arm7_arm_037fcf10((u32) (temp_r4 + 0x71C));
    return native_utility_child_arm7_arm_027e6848();
}
