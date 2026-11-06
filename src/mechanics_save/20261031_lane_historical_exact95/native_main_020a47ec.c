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
extern void native_fn_020a4d10(s32,u32,s32);
extern u32 native_fn_020a4d58(s32,s32,u32,u32);
extern u32 native_fn_020a4d88(void);
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
} Record_native_data_021d230c;
extern Record_native_data_021d230c native_data_021d230c;
u32 native_main_020a47ec(s32 arg0, s32 *arg1, u32 arg2) {
    s32 temp_r0;
    s32 var_r4;
    s32 var_r5;
    s32 sp4;
    s32 *sp0;

    var_r5 = arg0;
    var_r4 = native_data_021d230c.field_8;
    sp0 = arg1;
    sp4 = 0;
    do {
        if (*sp0 != 0) {
            do {
                native_fn_020a4d10(var_r4, 0x100, var_r5);
            } while (native_fn_020a4d58(var_r5, var_r4, 0x100, arg2) == 0);
        }
        sp0 += 1;
        var_r5 += 0x100;
        temp_r0 = sp4 + 1;
        sp4 = temp_r0;
        var_r4 += 0x100;
    } while (temp_r0 < 4);
    if (native_fn_020a4d88() != 0) {
        return 1U;
    }
    return 0U;
}
