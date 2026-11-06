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
extern u32 native_fn_02041908();
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
} Record_native_data_ov001_0223d8ec;
extern Record_native_data_ov001_0223d8ec native_data_ov001_0223d8ec;
u32 native_ov001_02203558(s32 arg0) {
    native_data_ov001_0223d8ec.field_8 = 8;
    if (arg0 != 0) {
        native_fn_02041538(1, 2, 0x1E);
        return native_fn_02041908(0x1E, 0xC);
    }
    return native_fn_02041538(1, 2, 0xA);
}
