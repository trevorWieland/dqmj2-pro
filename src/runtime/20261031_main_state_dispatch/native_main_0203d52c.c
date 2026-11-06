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
extern void native_fn_02002c98();
extern void native_fn_02002e5c();
extern void native_fn_020033e8();
extern void native_fn_020035c0();
extern void native_fn_02008c58();
extern void native_fn_02029c88();
extern void native_fn_02029cc4();
extern void native_fn_02029cf8();
extern void native_fn_02029d2c();
extern void native_fn_02029d5c();
extern void native_fn_0202abd8();
extern void native_fn_0203cb2c();
extern void native_fn_0203d30c();
extern void native_fn_0203d320();
extern void native_fn_0203d334();
extern void native_fn_0203d50c();
void native_main_0203d52c(void) {
    u16 temp_r0;

    native_fn_0202abd8(3, 0x10000);
    native_fn_0203d30c();
    native_fn_0203d320();
    native_fn_0203d334();
    native_fn_0203cb2c();
    native_fn_020033e8(0xB);
    native_fn_020035c0(0x10);
    native_fn_02002e5c(0x60);
    native_fn_02002c98(1, 0, 1);
    M2C_FIELD((void *)0x0400000A, u16 *, 0) = (u16) ((M2C_FIELD((void *)0x0400000A, u16 *, 0) & 0x43) | 0xD00);
    M2C_FIELD((void *)0x0400000A, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x0400000A, u16 *, 2) & 0x43) | 0xE00);
    native_fn_0203d50c(0);
    native_fn_02008c58(0, 0x06000000, 0x80000);
    *(s32 *)0x04000000 = (*(s32 *)0x04000000 & ~0x1F00) | 0xF00;
    native_fn_02029c88(0, 0, 0);
    native_fn_02029cc4(0x1F);
    native_fn_02029cf8(0x3F);
    native_fn_02029d2c(0);
    native_fn_02029d5c(0x7FFF);
    M2C_FIELD((void *)0x0400000A, u16 *, 0) = (u16) (M2C_FIELD((void *)0x0400000A, u16 *, 0) & ~3);
    M2C_FIELD((void *)0x0400000A, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x0400000A, u16 *, 4) & ~3) | 1);
    M2C_FIELD((void *)0x0400000A, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x0400000A, u16 *, 2) & ~3) | 2);
    temp_r0 = (*(u16 *)0x04000008 & ~3) | 3;
    *(u16 *)0x04000008 = temp_r0;
    return;
}
