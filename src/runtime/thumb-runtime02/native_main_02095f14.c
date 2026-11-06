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
extern u32 native_fn_020946ec();
extern u32 native_fn_02094790();
extern u32 native_fn_02098fbc();
u32 native_main_02095f14(void) {
    native_fn_020946ec(8);
    if (native_fn_02098fbc() != 0) {
        native_fn_02094790(3);
        return 0x11U;
    }
    return 0xEU;
}
