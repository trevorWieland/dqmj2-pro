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
extern u32 native_fn_02045dc4();
extern u8 native_data_020fab28[];
u32 native_main_02046ab4(s32 arg0, u32 arg1, u32 arg2, s32 arg3, u8 arg4) {
    return native_fn_02045dc4(arg0, (u8) M2C_FIELD(((arg0 * 0x90) + (s32) native_data_020fab28), s32 *, 4), arg1, arg2, arg3, (s32) arg4);
}
