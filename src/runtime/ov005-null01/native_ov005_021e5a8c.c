#define NULL ((void *)0)
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
extern u32 native_fn_02008e0c();
extern u32 native_fn_0207b1c4();
extern u32 native_fn_0207b460();
extern u32 native_fn_0207c078();
u32 native_ov005_021e5a8c(void *arg0, void *arg1) {
    if (arg1 == NULL) {
        M2C_FIELD(arg0, s16 *, 0x2E) = -1;
        M2C_FIELD(arg0, s32 *, 0) = -1;
        return -1U;
    }
    native_fn_02008e0c(arg1, arg0 + 0xB6, 0x14);
    M2C_FIELD(arg0, s32 *, 0) = (s32) M2C_FIELD(arg1, s16 *, 0x18);
    M2C_FIELD(arg0, s16 *, 0x2E) = (s16) M2C_FIELD(arg1, s16 *, 0x18);
    M2C_FIELD(arg0, u8 *, 0x30) = (u8) M2C_FIELD(arg1, u8 *, 0x1A);
    M2C_FIELD(arg0, s32 *, 4) = (s32) M2C_FIELD(arg1, s32 *, 0x14);
    M2C_FIELD(arg0, u8 *, 0xB1) = (u8) M2C_FIELD(arg1, u8 *, 0x1B);
    M2C_FIELD(arg0, u8 *, 0xB2) = (u8) M2C_FIELD(arg1, u8 *, 0x1E);
    M2C_FIELD(arg0, u8 *, 0xAF) = (u8) M2C_FIELD(arg1, u8 *, 0x1C);
    native_fn_02008e0c(arg1 + 0x7A, arg0 + 0xD6, 0xA);
    native_fn_02008e0c(arg1 + 0x40, arg0 + 0xE0, 0x3A);
    native_fn_02008e0c(arg1 + 0x20, arg0 + 0x11C, 0x20);
    native_fn_0207b460(M2C_FIELD(arg0, s16 *, 0x2E), M2C_FIELD(arg0, u8 *, 0x30), arg1 + 0x7A, arg0 + 0x4A);
    native_fn_0207b1c4(arg1 + 0x7A, arg0 + 0x4A, arg0 + 0xC);
    return native_fn_0207c078(M2C_FIELD(arg0, s16 *, 0x2E), M2C_FIELD(arg0, u8 *, 0x30), arg0 + 0x4A, arg0 + 0x8A);
}
