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
extern u32 native_fn_02003888();
extern u32 native_fn_02003db8();
extern u32 native_fn_02008c14();
extern u32 native_fn_0202a498();
typedef struct {
    s32 field_0;
    s32 field_4;
    s32 field_8;
    s32 field_c;
} Record_native_data_ov000_02246428;
extern Record_native_data_ov000_02246428 native_data_ov000_02246428;
u32 native_ov000_022218d4(void) {
    if (native_data_ov000_02246428.field_0 == 0) {
        return 0U;
    }
    native_fn_02008c14(0, 0x06840000, 0x18000);
    native_fn_02003db8();
    native_fn_02003888(native_data_ov000_02246428.field_c);
    native_fn_0202a498(1, native_data_ov000_02246428.field_8);
    native_data_ov000_02246428.field_8 = 0;
    native_fn_0202a498(1, native_data_ov000_02246428.field_4);
    native_data_ov000_02246428.field_4 = 0;
    return 1U;
}
