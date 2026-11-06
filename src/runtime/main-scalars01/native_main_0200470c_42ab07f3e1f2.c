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
extern u32 native_fn_0200845c();
extern u32 native_fn_020085b8();
extern u32 native_fn_02008c14();
extern u8 native_data_020dcb44[];
u32 native_main_0200470c(void) {
    s32 var_r2;

    if (*(u32 *)native_data_020dcb44 == -1) {
        goto block_2;
    }
    native_fn_020085b8(*(u32 *)native_data_020dcb44, 0x04000330, 0, 0x10, 0, 0);
    native_fn_0200845c(*(u32 *)native_data_020dcb44, 0x04000360, 0, 0x60);
    goto block_3;
block_2:
    native_fn_02008c14(0, 0x04000330, 0x10);
    native_fn_02008c14(0, 0x04000360, 0x60);
block_3:
    var_r2 = 0;
loop_4:
    var_r2 += 1;
    *(s32 *)0x040004D0 = 0;
    if (var_r2 < 0x20) {
        goto loop_4;
    }
    return 0x040004D0U;
}
