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
extern u32 native_fn_ov001_021fc908();
extern u32 native_fn_ov001_021fceb4();
extern u8 native_data_ov001_0222edc8[];
typedef struct {
    u8 unknown_0[0x70];
    s8 field_70;
} Record_native_data_ov001_02239d6c;
extern Record_native_data_ov001_02239d6c native_data_ov001_02239d6c;
u32 native_ov001_021fc5c4(void) {
    s8 var_r0;
    u8 *var_r2;

    native_data_ov001_02239d6c.field_70 = 0;
    *(s32 *)0x04001000 = (*(s32 *)0x04001000 & 0xFFCFFFEF) | 0x10;
    native_fn_ov001_021fc908();
    native_fn_ov001_021fceb4();
    var_r2 = native_data_ov001_0222edc8;
    var_r0 = 0;
    do {
        var_r0 += 1;
        *var_r2 = 0x7F;
        var_r2 += 1;
    } while ((s32) var_r0 < 3);
    return (u32) var_r0;
}
