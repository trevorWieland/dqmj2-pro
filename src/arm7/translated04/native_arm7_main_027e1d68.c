typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_arm7_fn_027e01cc(u32, u32, u32, u32);
u32 native_arm7_main_027e1d68(void *arg0, s16 arg1) {
    u16 temp_r1;
    u16 temp_r2;
    void *temp_r4;

    M2C_FIELD(arg0, s16 *, 0) = 0;
    M2C_FIELD(arg0, s16 *, 2) = 0;
    M2C_FIELD(arg0, s16 *, 4) = 0;
    M2C_FIELD(arg0, s16 *, 6) = 0;
    M2C_FIELD(arg0, s16 *, 8) = 0;
    M2C_FIELD(arg0, s16 *, 0xA) = 0;
    M2C_FIELD(arg0, u16 *, 0xC) = 0U;
    M2C_FIELD(arg0, u16 *, 0xE) = 1U;
    M2C_FIELD(arg0, s16 *, 0x10) = arg1;
    temp_r2 = M2C_FIELD(arg0, u16 *, 0xE);
    temp_r1 = M2C_FIELD(arg0, u16 *, 0xC);
    temp_r4 = arg0 + (temp_r2 * 2);
    M2C_FIELD(temp_r4, u16 *, 0x10) = temp_r1;
    M2C_FIELD(temp_r4, s16 *, 0x12) = 1;
    native_arm7_fn_027e01cc((u32) arg0, (u32) temp_r1, (u32) temp_r2, 1U);
    return (u32) (temp_r4 + 0x10);
}
