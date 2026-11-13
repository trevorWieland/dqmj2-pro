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
extern u32 native_fn_02063b18();
extern u32 native_fn_ov000_021f9cdc();
extern u32 ov000_display_context_02215698();
typedef struct {
    u8 field_0;
    u8 field_1;
} Record_native_data_ov000_0222f42c;
extern Record_native_data_ov000_0222f42c native_data_ov000_0222f42c;
u32 native_ov000_021fbdec(s32 arg0, u32 arg1, s32 arg2) {
    ov000_display_context_02215698();
    if (native_data_ov000_0222f42c.field_1 == 6) {
        return native_fn_ov000_021f9cdc(5, 6, native_data_ov000_0222f42c.field_0, arg1, arg2);
    }
    if (arg0 != 0) {
        return native_fn_ov000_021f9cdc(5, 6, 5U, arg1, 0);
    }
    if (native_fn_02063b18(0x3D) == 0) {
        return native_fn_ov000_021f9cdc(5, 6, 7U, arg1, 1);
    }
    return native_fn_ov000_021f9cdc(5, 6, 6U, arg1, 1);
}
