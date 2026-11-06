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
extern u32 native_fn_0200708c();
extern u32 native_fn_02007110();
extern u32 native_fn_0203c4bc();
extern u8 native_data_020edf20[];
extern u8 native_data_020edf2c[];
u32 native_main_0202acec(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 var_r4;

    var_r4 = 0;
    native_fn_0200708c(native_data_020edf2c);
    if (((s32) M2C_FIELD(native_data_020edf20, s16 *, 6) < (s32) M2C_FIELD(native_data_020edf20, s16 *, 4)) && (native_fn_0203c4bc(arg0, arg1, arg2, arg3) != 0)) {
        var_r4 = 1;
        M2C_FIELD(native_data_020edf20, s16 *, 6) = (s16) (M2C_FIELD(native_data_020edf20, s16 *, 6) + 1);
    }
    native_fn_02007110(native_data_020edf2c);
    return var_r4;
}
