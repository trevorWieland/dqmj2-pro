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
extern u32 native_fn_020a8640();
extern u32 native_fn_020a8644();
extern u32 native_fn_020a86ec();
extern u8 native_data_021d2bc4[];
u32 native_main_020b65f8(s32 arg0) {
    u32 var_r0;
    s32 var_r4;

    var_r4 = 0;
    var_r0 = native_fn_020a8640(*(u32 *)native_data_021d2bc4);
    if ((s32) var_r0 > 0) {
loop_2:
        if (arg0 == native_fn_020a8644(*(u32 *)native_data_021d2bc4, var_r4)) {
            return native_fn_020a86ec(*(u32 *)native_data_021d2bc4, var_r4);
        }
        var_r4 += 1;
        var_r0 = native_fn_020a8640(*(u32 *)native_data_021d2bc4);
        if (var_r4 >= (s32) var_r0) {
            
            return var_r0;
        }
        goto loop_2;
    }
    return var_r0;
}
