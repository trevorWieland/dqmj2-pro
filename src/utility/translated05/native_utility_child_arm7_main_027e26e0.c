typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e0698(u32);
u32 native_utility_child_arm7_main_027e26e0(void *arg0) {
    void *temp_r2;
    void *temp_r4;

    M2C_FIELD(arg0, s16 *, 0) = 0;
    M2C_FIELD(arg0, s16 *, 2) = 0;
    M2C_FIELD(arg0, s16 *, 4) = 0;
    M2C_FIELD(arg0, s16 *, 6) = 0;
    M2C_FIELD(arg0, s16 *, 8) = 0;
    M2C_FIELD(arg0, s16 *, 0xA) = 0;
    M2C_FIELD(arg0, u16 *, 0xC) = 0x200U;
    M2C_FIELD(arg0, u16 *, 0xE) = 0x48U;
    temp_r2 = arg0 + (M2C_FIELD(arg0, u16 *, 0xE) * 2);
    temp_r4 = temp_r2 + 0x10;
    M2C_FIELD(temp_r2, u16 *, 0x10) = (u16) M2C_FIELD(arg0, u16 *, 0xC);
    M2C_FIELD(temp_r4, s16 *, 2) = 1;
    native_utility_child_arm7_arm_027e0698((u32) arg0);
    return (u32) temp_r4;
}
