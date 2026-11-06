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
extern u32 native_fn_020c8fa8();
extern u32 native_fn_020c9984();
extern u32 native_fn_020c9a3c();
u32 native_main_020c9fb0(u32 arg0, u32 arg1) {
    u32 temp_r4;

    temp_r4 = arg0 >> 1;
    native_fn_020c9984(4, M2C_FIELD((void *) native_fn_020c8fa8(), s8 *, 0x10), 2, (u8) temp_r4, arg0, (s32) (u8) (0x1F - temp_r4), 2, 0, 1);
    return native_fn_020c9a3c(4, 9, 1, arg1, 0x10);
}
