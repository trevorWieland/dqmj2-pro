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
extern u32 native_fn_020850a0();
extern u32 native_fn_02085270();
extern u32 native_fn_020852b0();
extern u32 native_fn_02086b14();
extern u32 native_fn_02087e44();
u32 native_main_0204a0b0(void *arg0, u32 arg1) {
    native_fn_020850a0();
    native_fn_02087e44(M2C_FIELD(arg0, s32 *, 0x44), 0);
    native_fn_020852b0(arg0 + 0x3C, arg1);
    native_fn_02085270(arg0 + 0x3C, 0, 0);
    M2C_FIELD(arg0, s32 *, 0x18) = (s32) (M2C_FIELD(arg0, s32 *, 0x18) | 2);
    return native_fn_02086b14(arg0, 0x10);
}
