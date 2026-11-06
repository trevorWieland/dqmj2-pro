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
extern u32 native_fn_0207b004();
u32 native_ov001_021f03c8(s32 arg0, u32 arg1, void *arg2) {
    s32 var_r5;
    s8 temp_r0;

    var_r5 = arg0;
    if (native_fn_0207b004(arg1, 0x80) != 0) {
        temp_r0 = M2C_FIELD(arg2, s8 *, 0x231);
        if (temp_r0 == 1) {
            var_r5 = var_r5 >> 1;
        } else if (temp_r0 == 2) {
            var_r5 = var_r5 >> 2;
        }
    }
    return (u32) var_r5;
}
