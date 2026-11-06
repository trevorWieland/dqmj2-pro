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
extern u32 native_fn_0206259c();
extern u32 native_fn_02065d88();
extern u32 native_fn_0207c1e4();
u32 native_main_0207c2b8(void *arg0, u32 arg1) {
    s16 temp_r4;
    s32 var_r4;

    temp_r4 = M2C_FIELD(arg0, s16 *, 0);
    var_r4 = temp_r4 + native_fn_0207c1e4(arg1);
    if (native_fn_0206259c() == 0) {
        goto block_2;
    }
    var_r4 += M2C_FIELD((void *) native_fn_02065d88(M2C_FIELD(arg0, u8 *, 0x11)), u8 *, 0x21);
block_2:
    if (var_r4 < 0x270F) {
        goto block_4;
    }
    var_r4 = 0x270F;
block_4:
    return (u32) var_r4;
}
