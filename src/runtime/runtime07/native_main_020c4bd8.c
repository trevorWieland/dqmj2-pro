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
extern u32 native_fn_02045654();
extern u32 native_fn_02061944();
extern u8 native_data_020dc8ac[];
u32 native_main_020c4bd8(void) {
    s32 var_r1;

    if (M2C_FIELD((void *) native_fn_02061944(), s8 *, 0x273) != 0) {
        var_r1 = 2;
    } else {
        var_r1 = 1;
    }
    return native_fn_02045654(native_data_020dc8ac[var_r1]);
}
