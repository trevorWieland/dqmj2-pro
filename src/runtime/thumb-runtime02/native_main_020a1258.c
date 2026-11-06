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
extern u32 native_fn_020a2ff8();
extern u32 native_fn_020a304c();
extern u32 native_fn_020a3d70();
u32 native_main_020a1258(u32 arg0) {
    if (M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0x15) == 0) {
        return native_fn_020a304c(arg0);
    }
    return native_fn_020a2ff8(arg0);
}
