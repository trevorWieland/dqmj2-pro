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
extern u32 native_fn_02088380();
u32 native_main_02086ce8(void *arg0, s32 arg1, u32 arg2, u32 arg3, s16 arg4, u8 arg5) {
    return native_fn_02088380(M2C_FIELD(arg0, s32 *, 0x44), arg2, arg3, arg4, (s32) arg5, arg1);
}
