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
extern u32 native_fn_0207dd5c();
extern u32 native_fn_0207e4ac();
extern u32 native_fn_020c225c();
u32 native_main_02064488(u32 arg0) {
    u32 temp_r0;

    if (native_fn_0207e4ac() != 0) {
        goto block_2;
    }
    native_fn_020c225c(0x20000000);
block_2:
    temp_r0 = native_fn_0207dd5c(arg0);
    if (temp_r0 == 0) {
        goto block_4;
    }
    return temp_r0;
block_4:
    return native_fn_020c225c(0x20000000);
}
