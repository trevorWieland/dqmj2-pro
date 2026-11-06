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
extern u32 native_fn_ov005_021d99c4();
u32 native_ov005_021d9a10(void *arg0) {
    void *temp_r4;
    s32 var_r5;

    temp_r4 = M2C_FIELD(M2C_FIELD(M2C_FIELD(arg0, void **, 0x20), void **, 0xC), void **, 0x24);
    if ((s32) M2C_FIELD(temp_r4, s32 *, 0x41C) >= (s32) M2C_FIELD(temp_r4, s32 *, 0x424)) {
        return 0xFFFFU;
    }
    var_r5 = M2C_FIELD(temp_r4, s32 *, 0x414);
loop_3:
    var_r5 += 1;
    if ((var_r5 < (s32) M2C_FIELD(temp_r4, s32 *, 0x424)) && (var_r5 < (s32) (M2C_FIELD(temp_r4, s32 *, 0x41C) + 0x20))) {

    } else {
        var_r5 = M2C_FIELD(temp_r4, s32 *, 0x41C);
    }
    if (native_fn_ov005_021d99c4(arg0, var_r5) == 0) {
        M2C_FIELD(temp_r4, s32 *, 0x414) = var_r5;
        return (u32) (u16) var_r5;
    }
    if (var_r5 == M2C_FIELD(temp_r4, s32 *, 0x414)) {
        return 0xFFFFU;
    }
    goto loop_3;
}
