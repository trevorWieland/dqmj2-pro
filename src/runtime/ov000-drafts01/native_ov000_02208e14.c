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
extern u32 native_fn_02002e5c();
extern u32 native_fn_02003af4();
extern u32 native_fn_02008c58();
extern u32 native_fn_020481b8();
extern u32 native_fn_02048308();
u32 native_ov000_02208e14(u32 arg0) {
    s16 sp0;

    sp0 = 0;
    native_fn_02003af4();
    native_fn_02002e5c(arg0);
    *(u16 *)0x0400000A = (*(u16 *)0x0400000A & 0x43) | 8;
    native_fn_02008c58(0, 0x06000000, 0x80000);
    *(s32 *)0x04000000 = (*(s32 *)0x04000000 & ~0x1F00) | 0x300;
    native_fn_020481b8(&sp0, 0, 2);
    return native_fn_02048308();
}
