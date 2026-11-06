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
extern u32 native_fn_02041538();
extern u32 native_fn_0204157c();
extern u32 native_fn_02041908();
extern u32 native_fn_02041930();
extern u32 native_fn_020620b4();
extern u32 native_fn_02062358();
extern u32 native_fn_ov000_021eadf4();
typedef struct {
    u8 unknown_0[0x10];
    s8 field_10;
} Record_native_data_ov000_022460d4;
extern Record_native_data_ov000_022460d4 native_data_ov000_022460d4;
u32 native_ov000_0221be98(void) {
    s8 var_r4;

    var_r4 = native_data_ov000_022460d4.field_10;
    if ((var_r4 == 6) && (native_fn_ov000_021eadf4() != 0)) {
        native_fn_020620b4(1);
        native_fn_02062358(1);
        native_fn_02041930();
        native_fn_0204157c();
        native_fn_02041538(1, 2, 0xA);
        native_fn_02041908(0xA, 8);
        var_r4 = 7;
    }
    return (u32) var_r4;
}
