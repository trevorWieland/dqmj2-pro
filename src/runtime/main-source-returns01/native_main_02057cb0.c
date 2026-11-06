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
extern u32 native_fn_02044f9c();
extern u8 native_fn_02044fac();
extern u32 native_fn_02062a10();
extern u32 native_fn_0207c880();
extern u32 native_fn_0207c8a4();
extern u32 native_fn_0207c8fc();
extern u32 native_fn_0207c9b8();
u32 native_main_02057cb0(void) {
    u8 *temp_r0;
    u8 temp_r0_2;
    u32 temp_r4;

    temp_r0 = native_fn_02062a10();
    temp_r0_2 = native_fn_02044fac(M2C_FIELD(temp_r0, s16 *, 0x18), M2C_FIELD(temp_r0, u8 *, 0x1A));
    M2C_FIELD(temp_r0, u8 *, 0x30) = temp_r0_2;
    temp_r4 = native_fn_02044f9c(M2C_FIELD(temp_r0, s16 *, 0x18), M2C_FIELD(temp_r0, u8 *, 0x1A));
    native_fn_0207c880();
    native_fn_0207c8a4(1, temp_r4);
    M2C_FIELD(temp_r0, u32 *, 0x34) = native_fn_0207c9b8(temp_r4, temp_r0_2);
    M2C_FIELD(temp_r0, u32 *, 0x38) = native_fn_0207c9b8(temp_r4, temp_r0_2 + 1);
    return native_fn_0207c8fc(1);
}
