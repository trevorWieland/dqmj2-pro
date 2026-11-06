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
extern u32 native_fn_ov001_021d9494();
extern u32 native_fn_ov001_021da480();
extern u32 native_fn_ov001_021db438();
typedef struct {
    u8 unknown_0[0x1b];
    s8 field_1b;
    u8 unknown_1c[0x64];
    s32 field_80;
    s32 field_84;
} Record_native_data_ov001_0223989c;
extern Record_native_data_ov001_0223989c native_data_ov001_0223989c;
u32 native_ov001_021f8fd8(void) {
    s32 var_r6;
    s32 var_r6_2;

    native_fn_ov001_021d9494(native_data_ov001_0223989c.field_84, 0, 0);
    native_fn_ov001_021d9494(native_data_ov001_0223989c.field_80, 0, 0);
    var_r6 = 0;
    do {
        native_fn_ov001_021da480(native_fn_ov001_021db438(0, var_r6), 1);
        var_r6 += 1;
    } while (var_r6 < 3);
    var_r6_2 = 0;
    do {
        native_fn_ov001_021da480(native_fn_ov001_021db438(1, var_r6_2), 1);
        var_r6_2 += 1;
    } while (var_r6_2 < 3);
    native_data_ov001_0223989c.field_1b = 0x1C;
    return 1U;
}
