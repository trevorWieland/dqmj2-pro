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
extern u32 native_fn_0205e7a8();
extern u32 native_fn_ov000_02207bc0();
typedef struct {
    u8 unknown_0[0xf0];
    s8 field_f0;
    s8 field_f1;
} Record_native_data_ov000_022383e8;
extern Record_native_data_ov000_022383e8 native_data_ov000_022383e8;
u32 native_ov000_02208154(void) {
    native_data_ov000_022383e8.field_f1 = 1;
    native_fn_ov000_02207bc0();
    native_fn_02041538(1, 2, 0xA);
    native_data_ov000_022383e8.field_f0 = 0xB;
    native_fn_0205e7a8(-1, 0x53);
    return 1U;
}
