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
extern u32 native_fn_02042cd0();
u32 native_main_02042cec(u32 arg0, s32 arg1, s32 arg2) {
    s32 var_r2;
    s32 var_r4;
    u16 temp_r1;
    u32 var_r0;

    var_r4 = -1;
    var_r0 = native_fn_02042cd0();
    if (var_r0 == 0) {
        goto block_9;
    }
    var_r4 = 0xFFFF;
    var_r2 = 0;
loop_2:
    if (M2C_FIELD(var_r0, u16 *, 2) != arg1) {
        goto block_6;
    }
    temp_r1 = M2C_FIELD(var_r0, u16 *, 0);
    if ((s32) temp_r1 < arg2) {
        goto block_6;
    }
    if ((s32) temp_r1 >= var_r4) {
        goto block_6;
    }
    var_r4 = (s32) temp_r1;
block_6:
    var_r2 += 1;
    var_r0 += 6;
    if (var_r2 < 0x10) {
        goto loop_2;
    }
    if (var_r4 != 0xFFFF) {
        goto block_9;
    }
    var_r4 = -1;
block_9:
    return (u32) var_r4;
}
