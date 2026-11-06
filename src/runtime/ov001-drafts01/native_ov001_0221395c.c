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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02002d00();
extern u32 native_fn_020038a8();
extern u32 native_fn_02003950();
extern u32 native_fn_020039c0();
extern u32 native_fn_02003a40();
extern u32 native_fn_02045338();
extern u32 native_fn_02046150();
extern u32 native_fn_020489f0();
u32 native_ov001_0221395c(void) {
    native_fn_02002d00(0);
    native_fn_020038a8(4);
    native_fn_02003950(0x100);
    native_fn_020039c0(0);
    native_fn_02003a40(0);
    native_fn_02045338();
    native_fn_020489f0(1);
    native_fn_02046150(1, 0, 2);
    return native_fn_02046150(2, 2, 2);
}
