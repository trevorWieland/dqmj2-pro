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
extern u32 native_fn_ov000_021e0d78();
typedef struct {
    u8 unknown_0[0x279];
    s8 field_279;
    s8 field_27a;
    s8 field_27b;
    s8 field_27c;
    s8 field_27d;
} Record_native_data_ov000_022322d4;
extern Record_native_data_ov000_022322d4 native_data_ov000_022322d4;
typedef struct {
    u8 unknown_0[0x80];
    s16 field_80;
    s16 field_82;
} Record_native_data_ov000_022324d4;
extern Record_native_data_ov000_022324d4 native_data_ov000_022324d4;
u32 native_ov000_021e1c4c(s8 arg0, s8 arg1, s8 arg2, s8 arg3, s32 arg4, s16 arg5, s16 arg6) {
    native_fn_ov000_021e07f0(1);
    native_data_ov000_022322d4.field_279 = arg0;
    native_data_ov000_022322d4.field_27a = arg1;
    native_data_ov000_022322d4.field_27b = arg2;
    native_data_ov000_022322d4.field_27c = arg3;
    native_data_ov000_022322d4.field_27d = 0;
    native_data_ov000_022324d4.field_80 = arg5;
    native_data_ov000_022324d4.field_82 = arg6;
    if (arg4 != 0) {
        native_fn_ov000_021e0d78(arg1, 0, 1);
    }
    return 1U;
}
