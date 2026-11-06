typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_03804f78(u32, u32, u32, u32);
extern u32 native_utility_child_arm7_arm_037fe6ec(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_027e0698(u32);
u32 native_utility_child_arm7_main_027e29e4(void *arg0, s16 arg1, u32 arg2, u32 arg3, u16 arg4, u16 arg5, u16 arg6, u16 arg7, u16 arg8, u32 arg9) {
    void *temp_r1;
    void *temp_r4;

    M2C_FIELD(arg0, s16 *, 0) = 0;
    M2C_FIELD(arg0, s16 *, 2) = 0;
    M2C_FIELD(arg0, s16 *, 4) = 0;
    M2C_FIELD(arg0, s16 *, 6) = 0;
    M2C_FIELD(arg0, s16 *, 8) = 0;
    M2C_FIELD(arg0, s16 *, 0xA) = 0;
    M2C_FIELD(arg0, u16 *, 0xC) = 9U;
    M2C_FIELD(arg0, u16 *, 0xE) = (u16) (native_utility_child_arm7_arm_03804f78(arg8 + 1, 2U, arg2, arg3) + 0x17);
    M2C_FIELD(arg0, s16 *, 0x10) = arg1;
    native_utility_child_arm7_arm_037fe6ec(arg2, (u32) (arg0 + 0x12), 0x20U);
    M2C_FIELD(arg0, s16 *, 0x32) = (s16) arg3;
    M2C_FIELD(arg0, u16 *, 0x34) = arg4;
    M2C_FIELD(arg0, u16 *, 0x36) = arg5;
    M2C_FIELD(arg0, u16 *, 0x38) = arg6;
    M2C_FIELD(arg0, u16 *, 0x3A) = arg7;
    M2C_FIELD(arg0, u16 *, 0x3C) = arg8;
    native_utility_child_arm7_arm_037fe6ec(arg9, (u32) (arg0 + 0x3E), (u32) arg8);
    temp_r1 = arg0 + (M2C_FIELD(arg0, u16 *, 0xE) * 2);
    temp_r4 = temp_r1 + 0x10;
    M2C_FIELD(temp_r1, u16 *, 0x10) = (u16) M2C_FIELD(arg0, u16 *, 0xC);
    M2C_FIELD(temp_r4, s16 *, 2) = 1;
    native_utility_child_arm7_arm_027e0698((u32) arg0);
    return (u32) temp_r4;
}
