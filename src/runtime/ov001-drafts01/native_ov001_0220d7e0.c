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
extern u32 native_fn_0202ac08();
extern u32 native_fn_0205d790();
extern u32 native_fn_ov001_021eea10();
extern u32 ov001_effect_resource_create_021eec7c();
extern u8 native_data_ov001_0223e0e8[];
u32 native_ov001_0220d7e0(u32 arg0, u32 arg1) {
    native_fn_0202ac08(native_data_ov001_0223e0e8);
    native_fn_ov001_021eea10(arg1, 0);
    return ov001_effect_resource_create_021eec7c(arg1, arg0, native_fn_0205d790(arg1));
}
