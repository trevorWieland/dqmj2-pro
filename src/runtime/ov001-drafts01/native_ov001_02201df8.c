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
extern u32 native_fn_ov001_021fc574();
extern u32 native_fn_ov001_021fc62c();
extern u32 native_fn_ov001_022095f4();
typedef struct {
    u8 unknown_0[0xa];
    s8 field_a;
    u8 unknown_b[0x1d];
    s32 field_28;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
u32 native_ov001_02201df8(void) {
    s8 var_r5;
    s8 var_r6;

    native_fn_ov001_021fc62c();
    var_r6 = 0;
    do {
        var_r5 = 0;
loop_2:
        native_fn_ov001_021fc574(var_r6, var_r5);
        var_r5 += 1;
        if ((s32) var_r5 < 3) {
            goto loop_2;
        }
        var_r6 += 1;
    } while ((s32) var_r6 < 2);
    native_fn_ov001_022095f4(native_data_ov001_02239c10.field_28, 3);
    native_data_ov001_02239c10.field_a = 0x14;
    return 0U;
}
