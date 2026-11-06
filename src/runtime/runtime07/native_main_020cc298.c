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
extern u32 native_fn_02048e74();
extern u32 native_fn_020cc4a0();
extern u32 native_fn_020cc570();
extern u32 native_fn_020cc74c();
extern u32 native_fn_020cc7d8();
extern u32 native_fn_020cf1f0();
extern u32 native_fn_020cf25c();
extern u8 native_data_021d6728[];
extern u8 native_data_021d672c[];
u32 native_main_020cc298(void) {
    u32 temp_r4;

    native_fn_02048e74(native_data_021d672c, 0);
    temp_r4 = native_fn_0202a1e0(2U);
    native_fn_020cc4a0();
    native_fn_020cc570();
    native_fn_0202a1e0(temp_r4);
    native_fn_020cf1f0();
    native_fn_020cf25c(0);
    native_fn_020cc74c(0);
    native_fn_020cc7d8();
    M2C_FIELD(native_data_021d6728, s32 *, 8) = 0;
    return (u32) native_data_021d6728;
}
