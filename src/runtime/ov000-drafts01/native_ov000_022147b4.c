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
extern u32 native_fn_02041510();
extern u32 native_fn_ov000_022145fc();
extern u32 native_fn_ov000_02214654();
typedef struct {
    u8 unknown_0[0x3];
    u8 field_3;
} Record_native_data_ov000_02244efc;
extern Record_native_data_ov000_02244efc native_data_ov000_02244efc;
typedef struct {
    u8 unknown_0[0xe2];
    s16 field_e2;
    s16 field_e4;
} Record_native_data_ov000_02245228;
extern Record_native_data_ov000_02245228 native_data_ov000_02245228;
u32 native_ov000_022147b4(void) {
    u32 var_r4;

    var_r4 = 3;
    native_fn_ov000_022145fc();
    native_fn_ov000_02214654();
    if (native_data_ov000_02244efc.field_3 != 0) {
        native_fn_02041510(1, 2, 0xF);
        var_r4 = 4;
    }
    if (native_data_ov000_02245228.field_e4 != native_data_ov000_02245228.field_e2) {
        var_r4 = 4;
    }
    return var_r4;
}
