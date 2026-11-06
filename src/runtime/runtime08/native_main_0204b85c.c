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
extern u32 native_fn_02048a60();
extern u32 native_fn_02048a94();
extern u32 native_fn_02048a9c();
extern u32 native_fn_0204b178();
extern u32 native_fn_0205f8a0();
extern u32 native_fn_0205f98c();
extern u32 native_fn_0205f998();
extern u32 native_fn_0205fa4c();
u32 native_main_0204b85c(void *arg0, void *arg1, u8 arg2, u32 arg3, u8 arg4, u8 arg5, u8 arg6) {
    u32 temp_r0;

    native_fn_0205f998();
    M2C_FIELD(arg0, s16 *, 0x14) = (s16) M2C_FIELD(arg1, s16 *, 0);
    M2C_FIELD(arg0, s16 *, 0x16) = (s16) M2C_FIELD(arg1, s16 *, 2);
    M2C_FIELD(arg0, u8 *, 0x20) = arg2;
    M2C_FIELD(arg0, u8 *, 0x21) = arg4;
    M2C_FIELD(arg0, s32 *, 0) = (s32) arg6;
    M2C_FIELD(arg0, s8 *, 0x22) = 1;
    native_fn_0205f8a0(arg0, arg3, 2);
    temp_r0 = native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), 0);
    native_fn_0204b178(temp_r0, arg5);
    native_fn_02048a94(temp_r0, M2C_FIELD(arg0, u8 *, 0x20));
    native_fn_02048a9c(temp_r0, M2C_FIELD(arg0, u8 *, 0x21));
    native_fn_02048a60(temp_r0, M2C_FIELD(arg0, s16 *, 0x14), M2C_FIELD(arg0, s16 *, 0x16));
    native_fn_0205fa4c(arg0, 1);
    return 0U;
}
