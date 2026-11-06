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
extern u32 native_fn_02045ed0();
extern u32 native_fn_020643fc();
extern u32 native_fn_020ba564();
extern u32 native_fn_020d268c();
extern u32 native_fn_020d2720();
extern u32 native_fn_020d2b14();
extern u32 native_fn_020d2e68();
extern u8 native_data_020e32c8[];
extern u8 native_data_021d7098[];
u32 native_main_020d23e4(void) {
    u32 temp_r0;

    native_fn_020d2b14();
    native_fn_020d2e68();
    native_fn_02045ed0(1);
    native_fn_020d268c(native_fn_020643fc(M2C_FIELD(native_data_021d7098, u16 *, 0x22)), 0x10, 1);
    M2C_FIELD((void *)0x04000008, u16 *, 0) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 0) & ~3) | 2);
    M2C_FIELD((void *)0x04000008, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 4) & ~3) | 1);
    M2C_FIELD((void *)0x04000008, u16 *, 6) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 6) & ~3) | 3);
    M2C_FIELD(native_data_021d7098, s32 *, 8) = 0;
    temp_r0 = native_fn_020ba564();
    if (temp_r0 == 0) {
        return temp_r0;
    }
    *(s32 *)0x04000000 = (*(s32 *)0x04000000 & ~0x1F00) | 0x1F00;
    native_fn_020d2720(native_data_020e32c8, 4);
    M2C_FIELD(native_data_021d7098, s32 *, 8) = 1;
    return (u32) native_data_021d7098;
}
