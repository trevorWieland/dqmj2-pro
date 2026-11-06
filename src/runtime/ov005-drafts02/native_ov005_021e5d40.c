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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02062a50();
extern u32 native_fn_02062a88();
extern u32 native_fn_0207b460();
extern u32 native_fn_0207c2b8();
extern u32 native_fn_0207c3d8();
void native_ov005_021e5d40(void) {
    u8 sp0[64];
    u32 var_r6;
    u32 var_r0;

    var_r6 = 0;
loop_1:
    if (var_r6 >= 3U) {
        goto block_3;
    }
    var_r0 = native_fn_02062a50(var_r6);
    goto block_4;
block_3:
    var_r0 = native_fn_02062a88(var_r6 - 3);
block_4:
    if (var_r0 == 0) {
        goto block_6;
    }
    native_fn_0207b460(M2C_FIELD(var_r0, s16 *, 0x18), M2C_FIELD(var_r0, u8 *, 0x1A), var_r0 + 0x7A, &sp0);
    M2C_FIELD(var_r0, s16 *, 0x24) = (s16) native_fn_0207c2b8(var_r0 + 0x20, &sp0);
    M2C_FIELD(var_r0, s16 *, 0x26) = (s16) native_fn_0207c3d8(var_r0 + 0x20, &sp0);
    M2C_FIELD(var_r0, s8 *, 0x33) = 0;
block_6:
    var_r6 = (u32) (u8) (var_r6 + 1);
    if (var_r6 < 6U) {
        goto loop_1;
    }
    return;
}
