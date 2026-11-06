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
extern u32 native_fn_0202a1e0();
extern u32 native_fn_0204bcbc();
extern u32 native_fn_0205bcfc();
extern u8 native_data_ov000_02233ae8[];
u32 native_ov000_021e4db8(void) {
    u32 temp_r4;
    u32 temp_r5;

    temp_r5 = native_fn_0202a1e0(1U);
    native_fn_0205bcfc();
    temp_r4 = native_fn_0204bcbc(native_data_ov000_02233ae8);
    native_fn_0202a1e0(temp_r5);
    return temp_r4;
}
