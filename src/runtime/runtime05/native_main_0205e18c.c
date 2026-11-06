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
extern u32 native_fn_0202a1e0();
extern u32 native_fn_0202a51c();
extern u32 native_fn_0204bcbc();
extern u8 native_data_02106950[];
u32 native_main_0205e18c(void) {
    u32 temp_r4;

    temp_r4 = native_fn_0202a1e0(1U);
    native_fn_0204bcbc(M2C_FIELD(native_data_02106950, s32 *, 4));
    native_fn_0202a51c(M2C_FIELD(native_data_02106950, s32 *, 4));
    M2C_FIELD(native_data_02106950, s32 *, 4) = 0;
    return native_fn_0202a1e0(temp_r4);
}
