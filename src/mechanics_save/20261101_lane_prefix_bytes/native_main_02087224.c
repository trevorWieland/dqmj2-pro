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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
#define NULL ((void *)0)
extern u32 native_fn_02087294();
extern u32 native_fn_02087334(void *);
u32 native_main_02087224(void *arg0) {
    u32 temp_r2_2;
    u32 temp_r2_3;
    u8 temp_r2;

    if (((u32) (M2C_FIELD(arg0, u32 *, 0x80) << 0x1C) >> 0x1F) == 0) {
        return (u32) arg0;
    }
    if (++M2C_FIELD(arg0, u8 *, 0x85) <= 8U) {
        return (u32) arg0;
    }
    native_fn_02087334(arg0);
    temp_r2_2 = M2C_FIELD(arg0, u32 *, 0x80);
    temp_r2_3 = (temp_r2_2 & ~4) | ((u32) ((((u32) (temp_r2_2 << 0x1D) >> 0x1F) + 1) << 0x1F) >> 0x1D);
    M2C_FIELD(arg0, u32 *, 0x80) = temp_r2_3;
    native_fn_02087294(arg0, (u32) (temp_r2_3 << 0x1D) >> 0x1F);
    M2C_FIELD(arg0, u8 *, 0x85) = 0U;
    return 0U;
}
