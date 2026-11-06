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
u32 native_utility_child_arm7_main_027e22c4(void *arg0, s16 arg1, u32 arg2, u32 arg3) {
    void *temp_r1;
    void *temp_r5;

    M2C_FIELD(arg0, s16 *, 0) = 0;
    M2C_FIELD(arg0, s16 *, 2) = 0;
    M2C_FIELD(arg0, s16 *, 4) = 0;
    M2C_FIELD(arg0, s16 *, 6) = 0;
    M2C_FIELD(arg0, s16 *, 8) = 0;
    M2C_FIELD(arg0, s16 *, 0xA) = 0;
    M2C_FIELD(arg0, u16 *, 0xC) = 0x245U;
    M2C_FIELD(arg0, u16 *, 0xE) = (u16) (native_utility_child_arm7_arm_03804f78(arg1 + 1, 2U, arg2, arg3) + 1);
    M2C_FIELD(arg0, s16 *, 0x10) = arg1;
    native_utility_child_arm7_arm_037fe6ec(arg2, (u32) (arg0 + 0x12), (u32) arg1);
    temp_r1 = arg0 + (M2C_FIELD(arg0, u16 *, 0xE) * 2);
    temp_r5 = temp_r1 + 0x10;
    M2C_FIELD(temp_r1, u16 *, 0x10) = (u16) M2C_FIELD(arg0, u16 *, 0xC);
    M2C_FIELD(temp_r5, s16 *, 2) = 1;
    native_utility_child_arm7_arm_027e0698((u32) arg0);
    return (u32) temp_r5;
}
