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
extern u32 native_fn_02048f7c();
extern u32 native_fn_020c484c();
extern u32 native_fn_020c48bc();
extern u32 native_fn_020c48d0();
extern u32 native_fn_020c48e8();
u32 native_main_020cdd78(u32 arg0) {
    native_fn_020c48bc();
    switch (arg0) {
    default:
        break;
    case 1:
        native_fn_020c48d0(5, 6, 0x1B);
        break;
    case 2:
        native_fn_020c48d0(5, 6, 0x1C);
        break;
    case 3:
        native_fn_020c48d0(5, 6, 0x1D);
        break;
    case 4:
        native_fn_020c48d0(5, 6, 0x30);
        break;
    }
    native_fn_02048f7c(1);
    native_fn_020c484c();
    return native_fn_020c48e8(0x57);
}
