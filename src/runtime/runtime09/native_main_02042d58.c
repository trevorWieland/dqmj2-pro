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
extern u32 native_fn_02042c9c();
u32 native_main_02042d58(u32 arg0, s32 arg1, s32 *arg2) {
    s32 temp_r1;
    s32 var_r2;
    s32 var_r3;
    u32 temp_r0;
    u32 var_r4;

    var_r4 = 0;
    temp_r0 = native_fn_02042c9c();
    if (temp_r0 == 0) {
        goto block_9;
    }
    var_r2 = *arg2;
    if (var_r2 >= 0x10) {
        goto block_9;
    }
    var_r3 = (var_r2 * 6) + temp_r0;
loop_3:
    if (arg1 != M2C_FIELD(var_r3, u16 *, 8)) {
        goto block_8;
    }
    var_r4 = (var_r2 * 6) + (temp_r0 + 8);
    temp_r1 = var_r2 + 1;
    if (temp_r1 < 0x10) {
        goto block_6;
    }
    *arg2 = -1;
    goto block_7;
block_6:
    *arg2 = temp_r1;
block_7:
    goto block_9;
block_8:
    var_r2 += 1;
    var_r3 += 6;
    if (var_r2 < 0x10) {
        goto loop_3;
    }
block_9:
    return var_r4;
}
