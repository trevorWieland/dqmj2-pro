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
extern u32 native_fn_02003e88();
extern u32 native_fn_02003edc();
extern u32 native_fn_02003f80();
extern u32 native_fn_02004120();
extern u32 native_fn_02004174();
extern u32 native_fn_020041e4();
extern u32 native_fn_02008c58();
extern u32 native_fn_020c41bc();
extern u32 native_fn_020c4944();
u32 native_main_020c4960(void) {
    native_fn_020c4944();
    native_fn_02008c58(0, native_fn_02004120(), 0x8000);
    native_fn_02008c58(0, native_fn_02004174(), 0x4000);
    native_fn_02008c58(0, native_fn_020041e4(), 0x8000);
    native_fn_02008c58(0, native_fn_02003e88(), 0x800);
    native_fn_02008c58(0, native_fn_02003edc(), 0x800);
    native_fn_02008c58(0, native_fn_02003f80(), 0x800);
    return native_fn_020c41bc();
}
