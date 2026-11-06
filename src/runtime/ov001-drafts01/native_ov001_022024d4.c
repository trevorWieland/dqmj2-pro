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
extern u32 native_fn_ov001_021fd098();
extern u32 native_fn_ov001_02202598();
extern u32 native_fn_ov001_02204b14();
extern u32 native_fn_ov001_02204b2c();
u32 native_ov001_022024d4(s32 arg0, u32 arg1, s32 arg2) {
    u32 temp_r4;
    u32 var_r0;

    var_r0 = native_fn_ov001_021fd098();
    temp_r4 = var_r0;
    if (arg0 == 0) {
        var_r0 = native_fn_ov001_02202598(arg1);
    }
    if (temp_r4 == 0x7F) {
        return var_r0;
    }
    if (arg2 > 0) {
        return native_fn_ov001_02204b2c(temp_r4);
    }
    if (arg2 >= 0) {
        return var_r0;
    }
    return native_fn_ov001_02204b14(temp_r4);
}
