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
extern u32 native_fn_020a8614();
extern u32 native_fn_020a929c();
u32 native_main_020b42d4(void *arg0) {
    if (M2C_FIELD(arg0, s32 *, 0x38) != 0) {
        native_fn_020a929c();
    }
    if (M2C_FIELD(arg0, s32 *, 0x44) != 0) {
        native_fn_020a929c();
    }
    if (M2C_FIELD(arg0, s32 *, 0x50) != 0) {
        native_fn_020a929c();
    }
    if (M2C_FIELD(arg0, s32 *, 0x5C) != 0) {
        native_fn_020a8614();
    }
    if (M2C_FIELD(arg0, s32 *, 0x60) != 0) {
        native_fn_020a8614();
    }
    if (M2C_FIELD(arg0, s32 *, 0x98) != 0) {
        native_fn_020a8614();
    }
    if (M2C_FIELD(arg0, s32 *, 0x9C) != 0) {
        native_fn_020a8614();
    }
    return native_fn_020a929c(arg0);
}
