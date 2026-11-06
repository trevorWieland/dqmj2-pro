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
extern u32 native_fn_02029c88();
extern u32 native_fn_02040434();
extern u32 native_fn_02041800();
extern u32 native_fn_02041898();
extern u32 native_fn_020675a8();
extern u32 native_fn_ov000_02214344();
extern u32 native_fn_ov000_0221452c();
extern u32 native_fn_ov000_022145fc();
extern u32 native_fn_ov000_02214654();
extern u32 native_fn_ov000_022146c0();
extern u32 native_fn_ov000_022147b4();
typedef struct {
    u8 field_0;
    s8 field_1;
    u8 unknown_2[0x1];
    u8 field_3;
} Record_native_data_ov000_02244efc;
extern Record_native_data_ov000_02244efc native_data_ov000_02244efc;
typedef struct {
    u8 unknown_0[0x1e6];
    u8 field_1e6;
    u8 field_1e7;
} Record_native_data_ov000_02245128;
extern Record_native_data_ov000_02245128 native_data_ov000_02245128;
typedef struct {
    u8 unknown_0[0xe2];
    s16 field_e2;
    s16 field_e4;
} Record_native_data_ov000_02245228;
extern Record_native_data_ov000_02245228 native_data_ov000_02245228;
u32 native_ov000_0221480c(void) {
    u32 var_r4;

    var_r4 = 0;
    if ((native_fn_020675a8(1) != 0) && (native_fn_020675a8(3) != 0)) {
        native_data_ov000_02244efc.field_3 = 1U;
    }
    switch (native_data_ov000_02244efc.field_1) {
    default:
        break;
    case 0:
        if (native_fn_02041800() != 1) {
            native_data_ov000_02244efc.field_3 = 0U;
            native_fn_02029c88(0, 0, 0);
            native_fn_ov000_022146c0();
            native_data_ov000_02244efc.field_1 = 1;
        }
        break;
    case 1:
        native_data_ov000_02244efc.field_1 = (s8) native_fn_ov000_02214344();
        if ((s8) native_data_ov000_02244efc.field_0 != 0) {
            native_fn_ov000_022145fc();
            native_fn_ov000_02214654();
            native_data_ov000_02244efc.field_1 = 2;
        }
        break;
    case 2:
        if ((s8) native_data_ov000_02244efc.field_0 != 0) {
            native_fn_02041898(0);
            native_data_ov000_02244efc.field_0 = 0;
        }
        native_data_ov000_02244efc.field_1 = 3;
        break;
    case 3:
        native_data_ov000_02244efc.field_1 = (s8) native_fn_ov000_022147b4();
        break;
    case 4:
        native_data_ov000_02244efc.field_1 = (s8) native_fn_ov000_0221452c();
        native_data_ov000_02245228.field_e2 = (s16) native_data_ov000_02245228.field_e4;
        native_data_ov000_02245128.field_1e6 = (u8) native_data_ov000_02245128.field_1e7;
        if (native_data_ov000_02244efc.field_3 != 0) {
            native_data_ov000_02244efc.field_1 = 5;
        }
        break;
    case 5:
        if (native_fn_02041800() != 1) {
            native_fn_02040434();
            var_r4 = 1;
        }
        break;
    }
    return var_r4;
}
