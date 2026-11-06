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
extern u32 native_fn_0205fd0c();
extern u32 native_fn_0205fd34();
extern u32 native_fn_0205fd40();
extern u32 native_fn_0205fd70();
extern u32 native_fn_02062378();
extern u32 native_fn_02071b9c();
extern u32 native_fn_020cfad0();
extern u32 native_fn_020cfcf0();
extern u32 native_fn_020d0ad8();
extern u32 native_fn_020d0bfc();
u32 native_main_020d0218(u32 arg0, u32 arg1, u32 arg2) {
    if (native_fn_0205fd70() == 0) {
        goto block_8;
    }
    if (native_fn_02062378() != 6) {
        goto block_3;
    }
    native_fn_02071b9c();
block_3:
    native_fn_0205fd34(native_fn_0205fd70(), 0x10);
    if (native_fn_0205fd70() == 0) {
        goto block_8;
    }
loop_4:
    if (native_fn_02062378() == 6) {
        goto block_6;
    }
    native_fn_0205fd40();
    goto block_7;
block_6:
    native_fn_0205fd70();
    native_fn_0205fd0c();
block_7:
    if (native_fn_0205fd70() != 0) {
        goto loop_4;
    }
block_8:
    native_fn_020d0bfc(arg1);
    native_fn_020cfcf0();
    native_fn_020cfad0(arg0);
    return native_fn_020d0ad8(arg1, arg2);
}
