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
extern u32 native_fn_0205c1a8();
extern u32 native_fn_0205c1c0();
extern u32 native_fn_0205c1d0();
extern u32 native_fn_0205c1e8();
extern u32 native_fn_0205e644();
extern u32 native_fn_0205e66c();
extern u32 native_fn_0205e684();
extern u32 native_fn_0205e6ac();
extern u32 native_fn_0205e6c4();
extern u32 native_fn_0205e6ec();
extern u32 native_fn_0205e760();
extern u32 native_fn_0205e784();
extern u32 native_fn_0205e7e4();
extern u32 native_fn_0205e814();
extern u32 native_fn_ov000_021e7940();
extern u32 native_fn_ov000_021e7a78();
extern u32 native_fn_ov000_021e7aa8();
extern u32 native_fn_ov000_021e7b60();
u32 native_ov000_021e796c(s32 arg0, s32 arg1) {
    u32 var_r4;

    var_r4 = 0;
    if (arg0 != native_fn_0205c1e8()) {
        native_fn_ov000_021e7940(1);
        native_fn_0205e644();
        if (arg0 >= 0) {
            native_fn_0205e760(arg0);
        }
        native_fn_0205e66c();
        if (arg0 >= 0) {
            native_fn_0205e784(arg0);
        }
        native_fn_0205e6ac();
        if (arg0 >= 0) {
            native_fn_0205e7e4(0, arg0, -1);
        }
        native_fn_0205c1d0(arg0);
        native_fn_0205c1a8(0);
        var_r4 = 1;
    } else if (native_fn_0205c1c0() != 0) {
        native_fn_0205e684();
        if (arg0 >= 0) {
            native_fn_0205e784(arg0);
        }
        native_fn_0205e6ac();
        native_fn_ov000_021e7a78();
        native_fn_0205e814(0, 0x7F, 0xF);
        var_r4 = 1;
    } else {
        native_fn_0205e6c4();
    }
    if (arg1 != 0) {
        native_fn_ov000_021e7aa8();
        native_fn_ov000_021e7b60();
        native_fn_0205e6ec();
    }
    return var_r4;
}
