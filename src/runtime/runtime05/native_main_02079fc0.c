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
extern u32 native_fn_02049008();
extern u32 native_fn_02062aa0();
extern u32 native_fn_02062ad0();
extern u32 native_fn_02079800();
extern u32 native_fn_ov000_02217dbc();
extern u8 native_data_021c6638[];
u32 native_main_02079fc0(s32 arg0) {
    native_fn_02062aa0();
    native_fn_02062ad0();
    if ((arg0 != 1) && (arg0 != 8) && (arg0 != 9)) {

    } else {
        native_fn_02049008(native_data_021c6638, 5, 0, 1, 4);
    }
    native_fn_ov000_02217dbc();
    return native_fn_02079800();
}
