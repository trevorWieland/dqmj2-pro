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
extern u32 native_fn_020127ec();
extern u32 native_fn_020189b0();
extern u8 native_data_020ec360[];
u32 native_main_0201852c(void) {
    u32 var_r4;

    var_r4 = native_fn_020127ec(M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s32 *, 0x508));
    native_fn_020189b0(1, var_r4);
    if (var_r4 == 2) {
        var_r4 = 0;
    }
    return var_r4;
}
