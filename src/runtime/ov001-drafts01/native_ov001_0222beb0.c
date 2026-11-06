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
extern u32 native_fn_0203d294();
extern u32 native_fn_0206531c();
extern u32 native_fn_ov001_021e1358();
extern u32 native_fn_ov001_021f1294();
typedef struct {
    u8 field_0;
    s8 field_1;
} Record_native_data_ov001_022497e8;
extern Record_native_data_ov001_022497e8 native_data_ov001_022497e8;
u32 native_ov001_0222beb0(void) {
    u32 temp_r0;

    temp_r0 = native_fn_0206531c();
    switch (temp_r0) {
    default:
        break;
    case 1:
        native_data_ov001_022497e8.field_1 = 3;
        break;
    case 2:
        native_data_ov001_022497e8.field_1 = 4;
        break;
    case 4:
        native_data_ov001_022497e8.field_1 = 5;
        break;
    case 7:
        native_data_ov001_022497e8.field_1 = 6;
        break;
    }
    native_data_ov001_022497e8.field_0 = (u8) native_fn_0203d294(2);
    native_fn_ov001_021f1294(0x10, 2);
    native_fn_ov001_021e1358(native_data_ov001_022497e8.field_0);
    return 1U;
}
