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
extern u32 native_fn_020048a0();
extern u32 native_fn_020048f4();
extern u32 native_fn_0200494c();
extern u32 native_fn_020049a4();
extern u8 native_data_020fb2e8[];
extern u8 native_data_020fb4e8[];
extern u8 native_data_020fb6e8[];
extern u8 native_data_020fb8e8[];
u32 native_main_02048308(void) {
    native_fn_020048a0(native_data_020fb8e8, 0, 0x200);
    native_fn_0200494c(native_data_020fb6e8, 0, 0x200);
    native_fn_020048f4(native_data_020fb2e8, 0, 0x200);
    return native_fn_020049a4(native_data_020fb4e8, 0, 0x200);
}
