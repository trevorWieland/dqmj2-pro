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
extern u32 native_fn_02040384();
extern u32 native_fn_02041d78();
extern u32 native_fn_0205bd5c();
extern u32 native_fn_0205e18c();
extern u32 native_fn_0205e6c4();
extern u8 native_data_02106950[];
u32 native_main_0205e234(void) {
    native_fn_0205e6c4();
    native_fn_02040384();
    native_fn_0205bd5c();
    native_fn_02041d78();
    native_fn_0205e18c();
    return M2C_FIELD(native_data_02106950, u32 *, 0xC);
}
