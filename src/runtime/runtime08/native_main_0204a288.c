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
extern u32 native_fn_0204a154();
extern u32 native_fn_0204a808();
extern u8 native_data_020ddb10[];
u32 native_main_0204a288(u32 arg0, s16 *arg1, u32 arg2, u32 arg3, s32 arg4, s32 arg5, s32 arg6, s32 arg7) {
    s16 temp_r4;

    temp_r4 = *arg1;
    *arg1 += native_fn_0204a154(arg0, arg1, arg2, arg4, arg6, arg7);
    *arg1 += native_fn_0204a808(arg0, arg1, arg3, native_data_020ddb10, 0);
    *arg1 += native_fn_0204a154(arg0, arg1, arg3, arg5, arg6, 0);
    return *arg1 - temp_r4;
}
