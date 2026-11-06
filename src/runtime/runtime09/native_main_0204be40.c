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
extern u32 native_fn_020259b4();
u32 native_main_0204be40(s32 arg0, s32 arg1, u32 arg2) {
    if (arg1 != 0) {
        goto block_2;
    }
    return arg0 + 0x50 + (native_fn_020259b4(arg2) * 4);
block_2:
    if (arg1 != 1) {
        goto block_4;
    }
    return arg0 + 0x10 + (native_fn_020259b4(arg2) * 4);
block_4:
    if (arg1 == 3) {
        goto block_6;
    }
    return 0U;
block_6:
    return arg0 + 0x450 + (native_fn_020259b4(arg2) * 4);
}
