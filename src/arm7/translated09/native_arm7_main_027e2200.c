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
extern u32 native_arm7_fn_037fdf9c(u32, u32, u32);
extern u32 native_arm7_fn_027e01cc(u32);
u32 native_arm7_main_027e2200(void *arg0, u32 arg1) {
    void *temp_r5;

    M2C_FIELD(arg0, s16 *, 0) = 0;
    M2C_FIELD(arg0, s16 *, 2) = 0;
    M2C_FIELD(arg0, s16 *, 4) = 0;
    M2C_FIELD(arg0, s16 *, 6) = 0;
    M2C_FIELD(arg0, s16 *, 8) = 0;
    M2C_FIELD(arg0, s16 *, 0xA) = 0;
    M2C_FIELD(arg0, u16 *, 0xC) = 0x100U;
    M2C_FIELD(arg0, u16 *, 0xE) = 0x18U;
    native_arm7_fn_037fdf9c(arg1, (u32) (arg0 + 0x10), 0x30U);
    M2C_FIELD(arg1, s16 *, 2) = 0;
    M2C_FIELD(arg1, s16 *, 4) = 0;
    M2C_FIELD(arg1, s16 *, 8) = 0;
    M2C_FIELD(arg1, s16 *, 0xA) = 0;
    M2C_FIELD(arg1, s16 *, 0xC) = 0;
    M2C_FIELD(arg1, s16 *, 0x10) = 0;
    M2C_FIELD(arg1, s16 *, 0x12) = 0;
    M2C_FIELD(arg1, s16 *, 0x14) = 0;
    M2C_FIELD(arg1, s16 *, 0x16) = 0;
    M2C_FIELD(arg1, s16 *, 0x24) = 0;
    M2C_FIELD(arg1, s16 *, 0x26) = 0;
    M2C_FIELD(arg1, s16 *, 0x28) = 0;
    M2C_FIELD(arg1, s16 *, 0x2A) = 0;
    temp_r5 = arg0 + (M2C_FIELD(arg0, u16 *, 0xE) * 2);
    M2C_FIELD(temp_r5, u16 *, 0x10) = (u16) M2C_FIELD(arg0, u16 *, 0xC);
    M2C_FIELD(temp_r5, s16 *, 0x12) = 2;
    native_arm7_fn_027e01cc((u32) arg0);
    return (u32) (temp_r5 + 0x10);
}
