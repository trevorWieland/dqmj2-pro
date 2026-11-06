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
extern u32 native_fn_ov000_021e07f0();
extern u32 native_fn_ov000_021e1cc0();
extern u32 native_fn_ov000_021e2dcc();
typedef struct {
    u8 unknown_0[0x279];
    u8 field_279;
    u8 unknown_27a[0x4];
    s8 field_27e;
} Record_native_data_ov000_022322d4;
extern Record_native_data_ov000_022322d4 native_data_ov000_022322d4;
u32 native_ov000_021e1dfc(void) {
    u32 temp_r4;

    native_data_ov000_022322d4.field_27e = 1;
    temp_r4 = native_fn_ov000_021e2dcc();
    if (((s32) native_fn_ov000_021e1cc0() <= 0) && (temp_r4 != 0)) {
        native_fn_ov000_021e07f0(native_data_ov000_022322d4.field_279);
    }
    return 0U;
}
