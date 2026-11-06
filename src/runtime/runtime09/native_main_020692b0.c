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
extern u32 native_fn_02062a10();
extern u32 native_fn_02069068();
u32 native_main_020692b0(u32 arg0, s32 arg1, s32 arg2, s32 arg3, u8 arg4, u8 arg5, u8 arg6) {
    u32 temp_r4;
    u32 temp_r5;

    temp_r5 = native_fn_02062a10();
    temp_r4 = native_fn_02062a10(arg0);
    return native_fn_02069068(M2C_FIELD(temp_r5, s16 *, 0x18), M2C_FIELD(temp_r4, u8 *, 0x1A), M2C_FIELD((void *) native_fn_02062a10(arg0), u8 *, 0x1D), arg0, arg1, arg2, arg3, (s32) arg4, (s32) arg5, (s32) arg6, 0);
}
