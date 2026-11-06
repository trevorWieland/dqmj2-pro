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
extern u32 native_fn_02008430();
extern u32 native_fn_02008d78();
extern u32 native_fn_0200a2c4();
extern u32 native_fn_0200dbc0();
extern u32 native_fn_0200dc38();
extern u32 native_fn_0200dccc();
extern u8 native_data_021c36c4[];
extern u8 native_data_021c36d0[];
u32 native_main_02066a9c(void) {
    native_fn_0200a2c4();
    native_fn_0200dbc0();
    if (native_fn_0200dc38(native_data_021c36d0) == 0) {
        native_fn_02008430();
    }
    native_fn_0200dccc(native_data_021c36d0);
    return native_fn_02008d78(native_data_021c36c4, 0, 4);
}
