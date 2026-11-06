typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe6ec(u32, u32, u32, u32);
extern u32 native_utility_child_arm7_arm_027e0698(u32);
u32 native_utility_child_arm7_main_027e25a0(void *arg0, u32 arg1, u32 arg2, u32 arg3) {
    void *temp_r1;
    void *temp_r5;

    M2C_FIELD(arg0, s16 *, 0) = 0;
    M2C_FIELD(arg0, s16 *, 2) = 0;
    M2C_FIELD(arg0, s16 *, 4) = 0;
    M2C_FIELD(arg0, s16 *, 6) = 0;
    M2C_FIELD(arg0, s16 *, 8) = 0;
    M2C_FIELD(arg0, s16 *, 0xA) = 0;
    M2C_FIELD(arg0, u16 *, 0xC) = 0x20DU;
    M2C_FIELD(arg0, u16 *, 0xE) = 0x10U;
    native_utility_child_arm7_arm_037fe6ec(arg1, (u32) (arg0 + 0x10), 0x20U, arg3);
    temp_r1 = arg0 + (M2C_FIELD(arg0, u16 *, 0xE) * 2);
    temp_r5 = temp_r1 + 0x10;
    M2C_FIELD(temp_r1, u16 *, 0x10) = (u16) M2C_FIELD(arg0, u16 *, 0xC);
    M2C_FIELD(temp_r5, s16 *, 2) = 1;
    native_utility_child_arm7_arm_027e0698((u32) arg0);
    return (u32) temp_r5;
}
