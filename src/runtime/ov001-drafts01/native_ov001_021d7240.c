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
extern u32 native_fn_02028264();
extern u32 native_fn_02028280();
extern u32 native_fn_020282a8();
extern u32 native_fn_0202834c();
extern u32 native_fn_0202838c();
extern u32 native_fn_020283b4();
extern u32 native_fn_020283dc();
extern u32 native_fn_020283fc();
extern u32 native_fn_0202841c();
extern u8 native_data_ov001_0222fd50[];
u32 native_ov001_021d7240(void) {
    native_fn_02008d78(native_data_ov001_0222fd50, 0, 0x176C);
    M2C_FIELD(native_data_ov001_0222fd50, s16 *, 0x4C) = -1;
    native_fn_02028264();
    native_fn_02028280(native_data_ov001_0222fd50);
    native_fn_020282a8(0, 0x1E000);
    native_fn_0202834c(0, 0x1555);
    native_fn_0202838c(0, 0x1000);
    native_fn_020283b4(0, 0x1F4000);
    native_fn_0202841c(0, 0);
    native_fn_020283fc(0, 0, 0, 0);
    return native_fn_020283dc(0, 0, 0, 0);
}
