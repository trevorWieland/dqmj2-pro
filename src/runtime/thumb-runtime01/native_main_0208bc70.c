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
extern u32 native_fn_0208bc30();
extern u32 native_fn_0208bc58();
extern u8 native_data_021cfcf8[];
u32 native_main_0208bc70(s32 arg0) {
    s32 var_r1;
    s32 var_r2;
    s32 var_r4;
    u32 var_r6;

    var_r6 = 1;
    var_r4 = 1;
    var_r1 = 1;
    var_r2 = 1;
    if ((M2C_FIELD(native_data_021cfcf8, s32 *, 0x50) != 0) && (arg0 != M2C_FIELD(native_data_021cfcf8, s32 *, 0x50))) {
        var_r2 = 0;
    }
    if ((var_r2 == 0) && (arg0 != 0x7F000001)) {
        var_r1 = 0;
    }
    if ((var_r1 == 0) && (native_fn_0208bc30(arg0) == 0)) {
        var_r4 = 0;
    }
    if ((var_r4 == 0) && (native_fn_0208bc58(arg0) == 0)) {
        var_r6 = 0;
    }
    return var_r6;
}
