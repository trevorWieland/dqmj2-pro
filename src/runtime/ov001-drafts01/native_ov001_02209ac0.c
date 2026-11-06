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
u32 native_ov001_02209ac0(void *arg0) {
    s32 var_r4;
    s32 var_r7;
    s32 var_r7_2;
    u32 temp_r0;
    u32 temp_r0_2;

    var_r4 = 0;
    var_r7 = 0;
    do {
        temp_r0 = native_fn_02062a50(var_r7);
        if ((temp_r0 != 0) && (M2C_FIELD(temp_r0, s32 *, 0x14) == *M2C_FIELD(arg0, s32 **, 0x1E8))) {
            var_r4 = 1;
        }
        var_r7 += 1;
    } while (var_r7 < 3);
    var_r7_2 = 0;
    do {
        temp_r0_2 = native_fn_02062a88(var_r7_2);
        if ((temp_r0_2 != 0) && (M2C_FIELD(temp_r0_2, s32 *, 0x14) == *M2C_FIELD(arg0, s32 **, 0x1E8))) {
            var_r4 = 1;
        }
        var_r7_2 += 1;
    } while (var_r7_2 < 3);
    if (var_r4 == 0) {
        return 1U;
    }
    return 0U;
}
