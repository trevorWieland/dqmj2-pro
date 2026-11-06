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
extern u32 native_fn_020baf40();
extern u32 native_fn_020bafe8();
extern u32 native_fn_020bb0a0();
u32 native_main_020bb06c(u32 arg0) {
    s32 temp_r0_2;
    u32 temp_r0;

    temp_r0 = native_fn_020bafe8();
    if (temp_r0 == -1U) {
        goto block_2;
    }
    return temp_r0;
block_2:
    temp_r0_2 = (s32) native_fn_020baf40();
    if (temp_r0_2 >= 0) {
        goto block_4;
    }
    return -1U;
block_4:
    return native_fn_020bb0a0(temp_r0_2, arg0);
}
