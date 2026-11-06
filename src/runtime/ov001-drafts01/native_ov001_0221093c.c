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
extern u32 native_fn_ov001_0220ee84();
u32 native_ov001_0221093c(void *arg0, u32 arg1) {
    s32 var_r4;
    u32 var_r1;
    u8 temp_r0;

    var_r1 = arg1;
    var_r4 = 0;
loop_1:
    temp_r0 = M2C_FIELD((M2C_FIELD(arg0, s32 *, 0x1E8) + var_r4), u8 *, 0x46);
    if (temp_r0 != 0) {
        if (temp_r0 == 0x3D) {
            var_r1 = native_fn_ov001_0220ee84(var_r1);
        }
        var_r4 += 1;
        if (var_r4 < 0x40) {
            goto loop_1;
        }
    }
    return var_r1;
}
