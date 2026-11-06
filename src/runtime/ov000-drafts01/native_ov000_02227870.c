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
extern u32 native_fn_020c5dc4();
extern u32 native_fn_020c9414();
extern u32 native_fn_ov000_02224b84();
extern u32 native_fn_ov000_02224e38();
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
    u8 unknown_c[0x8];
    u32 field_14;
} Record_native_data_ov000_022468b8;
extern Record_native_data_ov000_022468b8 native_data_ov000_022468b8;
u32 native_ov000_02227870(void) {
    switch (native_data_ov000_022468b8.field_8) {
    case 0:
        native_data_ov000_022468b8.field_8 = 1;
        break;
    case 1:
        if (native_fn_020c5dc4() != 1) {
            native_data_ov000_022468b8.field_14 = native_fn_ov000_02224e38();
            native_data_ov000_022468b8.field_8 = 0;
        }
        native_fn_020c9414(2);
        break;
    case 2:
        native_data_ov000_022468b8.field_14 = native_fn_ov000_02224b84(1);
        native_data_ov000_022468b8.field_8 = 0;
        break;
    }
    return 0U;
}
