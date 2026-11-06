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
extern u32 native_fn_02008d78();
extern u32 native_fn_02044ff4();
extern u32 native_fn_02048034();
extern u32 native_fn_020642f8();
u32 native_ov006_021dcd40(void) {
    u32 temp_r4;
    u8 sp0[32];

    native_fn_02008d78(&sp0, 0, 0x20);
    temp_r4 = native_fn_020642f8();
    native_fn_02044ff4(&sp0, M2C_FIELD(temp_r4, u16 *, 2), M2C_FIELD((void *) native_fn_020642f8(), u8 *, 6));
    return native_fn_02048034(&sp0, 0);
}
