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
extern u32 native_fn_020456ac();
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u32 native_fn_0204861c();
extern u32 native_fn_02048f6c();
extern u32 native_fn_020622ec();
extern u8 native_data_020e32c4[];
extern u8 native_data_021d7098[];
extern u8 native_data_021d715c[];
void native_main_020d253c(void) {
    if (M2C_FIELD(native_data_021d7098, s32 *, 8) != 1) {
        goto block_2;
    }
    native_fn_0204861c(0, M2C_FIELD(native_data_021d715c, u8 *, 0x81));
    native_fn_020485b4(M2C_FIELD(native_data_021d7098, s32 *, 4));
    native_fn_020484dc(0, *native_data_020e32c4);
block_2:
    native_fn_020456ac(0, native_fn_02048f6c(0), 0x10, 1, 2, 2);
    native_fn_020622ec(6, 0x1C, 0);
    M2C_FIELD((void *)0x0400000A, u16 *, 0) = (u16) (M2C_FIELD((void *)0x0400000A, u16 *, 0) & ~3);
    M2C_FIELD((void *)0x0400000A, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x0400000A, u16 *, 4) & ~3) | 3);
    M2C_FIELD((void *)0x0400000A, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x0400000A, u16 *, 2) & ~3) | 2);
    *(u16 *)0x04000008 = (*(u16 *)0x04000008 & ~3) | 1;
    return;
}
