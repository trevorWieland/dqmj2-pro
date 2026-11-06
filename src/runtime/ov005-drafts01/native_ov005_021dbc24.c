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
extern u32 native_fn_02061de4();
extern u32 native_fn_02065818();
extern u8 native_data_ov005_021e9894[];
u32 native_ov005_021dbc24(s32 arg0, u32 arg1) {
    s32 temp_r4;

    temp_r4 = arg0 * 0xC;
    native_fn_02061de4(native_data_ov005_021e9894 + temp_r4, arg1, arg0 + 9, 0, 1);
    return native_fn_02065818(native_data_ov005_021e9894 + temp_r4, 0x1A, (s8) ((arg0 * 8) + 2));
}
