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
extern u32 native_fn_0206b324();
extern u32 native_fn_0206b340();
extern u32 native_fn_020c8fa8();
u32 native_main_020cae74(void) {
    s8 temp_r0;

    temp_r0 = M2C_FIELD((void *) native_fn_020c8fa8(), s8 *, 0x10);
    if (temp_r0 == 1) {
        goto block_6;
    }
    if (temp_r0 == 6) {
        goto block_4;
    }
    if (temp_r0 == 7) {
        goto block_4;
    }
    goto block_5;
block_4:
    goto block_7;
block_5:
    return (u32) temp_r0;
block_6:
    return native_fn_0206b324(0);
block_7:
    return native_fn_0206b340(0);
}
