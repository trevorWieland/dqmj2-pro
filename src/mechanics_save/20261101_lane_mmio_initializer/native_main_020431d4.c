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
#define NULL ((void *)0)
extern u32 native_fn_02002c98(u32, u32, u32);
extern u32 native_fn_02002e5c(u32);
extern u32 native_fn_020030ec(u32);
extern u32 native_fn_020033e8(u32);
extern u32 native_fn_020035c0(u32);
extern u32 native_fn_02008c58(u32, void *, u32);
extern u32 native_fn_0202abd8(u32 arg0, u32 arg1);
extern u32 native_fn_0203cb2c(void);
extern u32 native_fn_0203d30c(u32 arg0);
extern u32 native_fn_0203d320(u32 arg0);
extern u32 native_fn_0203d334(u32 arg0);
u32 native_main_020431d4(void) {
    native_fn_0203d334(native_fn_0203d320(native_fn_0203d30c(native_fn_0202abd8(3U, 0x10000U))));
    native_fn_0203cb2c();
    native_fn_020033e8(0xB);
    native_fn_020035c0(0x10);
    native_fn_02002e5c(0x20);
    native_fn_020030ec(0x40);
    native_fn_02002c98(1, 0, 1);
    *(volatile u32 *)0x04000000 = (*(volatile u32 *)0x04000000 & 0xFFCFFFEF) | 0x10;
    native_fn_02008c58(0, (void *)0x06000000, 0x80000);
    native_fn_02008c58(0, (void *)0x06400000, 0x40000);
    native_fn_02008c58(0, (void *)0x07000000, 0x400);
    *(volatile u16 *)0x04000060 = (*(volatile u16 *)0x04000060 & ~0x3000) | 8;
    *(volatile u16 *)0x0400000A = (*(volatile u16 *)0x0400000A & 0x43) | 0x700;
    *(volatile u16 *)0x0400000C = (*(volatile u16 *)0x0400000C & 0x43) | 0x600;
    *(volatile u32 *)0x04000000 = (s32) ((*(volatile u32 *)0x04000000 & ~0x1F00) | 0x1700);
    *(volatile u16 *)0x04000008 = (*(volatile u16 *)0x04000008 & ~3) | 3;
    *(volatile u16 *)0x0400000C = (*(volatile u16 *)0x0400000C & ~3) | 2;
    *(volatile u16 *)0x0400000E = (*(volatile u16 *)0x0400000E & ~3) | 1;
    *(volatile u16 *)0x0400000A &= ~3;
    return 0x0400000AU;
}
