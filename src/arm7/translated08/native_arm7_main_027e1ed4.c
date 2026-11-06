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
u32 native_arm7_main_027e1ed4(void *arg0, s16 arg1, u32 arg2) {
    void *temp_r5;

    M2C_FIELD(arg0, s16 *, 0) = 0;
    M2C_FIELD(arg0, s16 *, 2) = 0;
    M2C_FIELD(arg0, s16 *, 4) = 0;
    M2C_FIELD(arg0, s16 *, 6) = 0;
    M2C_FIELD(arg0, s16 *, 8) = 0;
    M2C_FIELD(arg0, s16 *, 0xA) = 0;
    M2C_FIELD(arg0, u16 *, 0xC) = 3U;
    M2C_FIELD(arg0, u16 *, 0xE) = 0x22U;
    M2C_FIELD(arg0, s16 *, 0x10) = arg1;
    M2C_FIELD(arg0, s16 *, 0x12) = 0;
    native_arm7_fn_037fdf9c(arg2, (u32) (arg0 + 0x14), 0x44U);
    temp_r5 = arg0 + (M2C_FIELD(arg0, u16 *, 0xE) * 2);
    M2C_FIELD(temp_r5, u16 *, 0x10) = (u16) M2C_FIELD(arg0, u16 *, 0xC);
    M2C_FIELD(temp_r5, s16 *, 0x12) = 5;
    native_arm7_fn_027e01cc((u32) arg0);
    return (u32) (temp_r5 + 0x10);
}
