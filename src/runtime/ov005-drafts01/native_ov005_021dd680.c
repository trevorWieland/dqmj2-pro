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
extern u32 native_fn_020414b0();
extern u32 native_fn_02041510();
extern u8 native_data_ov005_021e9818[];
u32 native_ov005_021dd680(void) {
    native_fn_020414b0(0x3F);
    native_fn_02041510(1, 2, 0xA);
    M2C_FIELD(native_data_ov005_021e9818, s8 *, 4) = 0xC;
    M2C_FIELD(native_data_ov005_021e9818, s8 *, 2) = 2;
    M2C_FIELD(native_data_ov005_021e9818, s16 *, 0xA) = 0;
    return (u32) native_data_ov005_021e9818;
}
