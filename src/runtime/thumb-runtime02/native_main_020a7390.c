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
extern u32 native_fn_020a7090();
extern u32 native_fn_020a7404();
extern u32 native_fn_020a762c();
extern u32 native_fn_020a8c24();
u32 native_main_020a7390(void *arg0, u32 arg1, u32 arg2) {
    u32 sp8;
    u32 sp4;
    s32 var_r4;
    u32 temp_r0;
    u32 temp_r0_2;

    var_r4 = 1;
loop_1:
    var_r4 -= 1;
    temp_r0 = native_fn_020a8c24(M2C_FIELD(arg0, s32 *, 0x6B4), arg1, arg2, 0);
    sp4 = temp_r0;
    if (((s32) temp_r0 <= 0) && (var_r4 >= 0) && ((s32) M2C_FIELD(arg0, s32 *, 0x80) <= 0)) {
        native_fn_020a762c(arg0);
        temp_r0_2 = native_fn_020a7404(arg0, 0, 0, 2, 0);
        sp8 = temp_r0_2;
        if (temp_r0_2 != 0) {
            native_fn_020a7090(arg0);
            return sp8;
        }
        if (var_r4 < 0) {
            goto block_7;
        }
        goto loop_1;
    }
block_7:
    if ((s32) sp4 <= 0) {
        return 3U;
    }
    return 0U;
}
