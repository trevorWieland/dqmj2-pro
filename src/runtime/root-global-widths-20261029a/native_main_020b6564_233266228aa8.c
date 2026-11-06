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
extern u32 native_fn_020a8640();
extern u32 native_fn_020a8644();
extern u8 native_data_021d2bc4[];
u32 native_main_020b6564(s32 arg0) {
    u8 *var_r0;
    s32 var_r4;

    if (*(u32 *)native_data_021d2bc4 == 0) {
        return 0U;
    }
    var_r4 = 0;
    if ((s32) native_fn_020a8640() > 0) {
loop_4:
        var_r0 = native_fn_020a8644(*(u32 *)native_data_021d2bc4, var_r4);
        if (M2C_FIELD(var_r0, s32 *, 8) != arg0) {
            var_r4 += 1;
            if (var_r4 >= (s32) native_fn_020a8640(*(u32 *)native_data_021d2bc4)) {
                goto block_6;
            }
            goto loop_4;
        }
    } else {
block_6:
        var_r0 = NULL;
    }
    return (u32) var_r0;
}
