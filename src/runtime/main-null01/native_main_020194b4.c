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
extern u32 native_fn_0200a2c4();
extern u32 native_fn_0200a3d0();
extern u32 native_fn_0200a41c();
extern u32 native_fn_0201919c();
extern u32 native_fn_0201946c();
extern u32 native_fn_02019568();
extern u32 native_fn_0201975c();
extern u32 native_fn_02019788();
extern u32 native_fn_020197f8();
extern u32 native_fn_0201980c();
extern u8 native_data_020ec3c0[];
extern u8 native_data_020ec4a0[];
u32 native_main_020194b4(void) {
    if (M2C_FIELD(native_data_020ec3c0, s32 *, 8) != 0) {
        return (u32) native_data_020ec3c0;
    }
    M2C_FIELD(native_data_020ec3c0, s32 *, 8) = 1;
    native_fn_0201919c();
    M2C_FIELD(native_data_020ec3c0, s32 *, 0xC) = 0;
    native_fn_0200a2c4();
    do {

    } while (native_fn_0200a41c(0xD, 1) == 0);
    native_fn_0200a3d0(0xD, native_fn_0201975c);
    native_fn_02019568();
    native_fn_0200a3d0(0xD, NULL);
    native_fn_0200a3d0(0xD, native_fn_02019788);
    M2C_FIELD(native_data_020ec3c0, s32 *, 0x18) = 0;
    native_fn_0201980c(native_data_020ec4a0);
    native_fn_0200a3d0(0x11, native_fn_020197f8);
    return native_fn_0201946c(0);
}
