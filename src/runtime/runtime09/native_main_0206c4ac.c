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
extern u32 native_fn_02044dc4();
extern u32 native_fn_02067748();
extern u32 native_fn_0206c49c();
u32 native_main_0206c4ac(u32 arg0, u32 arg1, s32 arg2) {
    s32 temp_r0;

    if (native_fn_0206c49c() == 0) {
        goto block_14;
    }
    temp_r0 = M2C_FIELD((void *) native_fn_02067748(), s32 *, 4);
    if (temp_r0 == 1) {
        goto block_5;
    }
    if (temp_r0 == 2) {
        goto block_7;
    }
    if (temp_r0 == 3) {
        goto block_10;
    }
    goto block_12;
block_5:
    if (native_fn_02044dc4(arg0, arg1) <= 3U) {
        goto block_12;
    }
    return 1U;
block_7:
    if (native_fn_02044dc4(arg0, arg1) < 4U) {
        goto block_9;
    }
    if (native_fn_02044dc4(arg0, arg1) <= 6U) {
        goto block_12;
    }
block_9:
    return 1U;
block_10:
    if (native_fn_02044dc4(arg0, arg1) >= 7U) {
        goto block_12;
    }
    return 1U;
block_12:
    if (arg2 == 0) {
        goto block_14;
    }
    return 1U;
block_14:
    return 0U;
}
