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
extern u32 native_fn_0202a498();
extern u32 native_fn_020847d0();
extern u32 native_fn_020c49e8();
extern u32 native_fn_ov000_021eef38();
extern u32 native_fn_ov000_021f0618();
extern u8 native_data_ov000_02236bc4[];
u32 native_ov000_021eed08(void) {
    native_fn_020847d0(2);
    native_fn_ov000_021f0618();
    native_fn_ov000_021eef38();
    native_fn_020c49e8();
    native_fn_0202a498(2, M2C_FIELD(native_data_ov000_02236bc4, s32 *, 4));
    M2C_FIELD(native_data_ov000_02236bc4, s32 *, 4) = 0;
    return (u32) native_data_ov000_02236bc4;
}
