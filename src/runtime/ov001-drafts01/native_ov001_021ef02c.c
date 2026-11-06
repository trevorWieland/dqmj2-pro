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
u32 native_ov001_021ef02c(void *arg0, u32 arg1, s32 arg2) {
    s32 var_r4;
    u32 temp_r0;
    u32 temp_r0_2;

    var_r4 = arg2;
    if (native_fn_0207b004(arg1, 0x400) != 0) {
        temp_r0 = M2C_FIELD(arg0, s8 *, 0x22D) + 2;
        switch (temp_r0) {
        default:
            break;
        case 4:
            var_r4 *= 2;
            break;
        case 3:
            temp_r0_2 = var_r4 * 3;
            var_r4 = (s32) (temp_r0_2 + (temp_r0_2 >> 0x1F)) >> 1;
            break;
        case 1:
            var_r4 = (s32) (var_r4 + ((u32) var_r4 >> 0x1F)) >> 1;
            break;
        case 0:
            var_r4 = (s32) (var_r4 + ((u32) (var_r4 >> 1) >> 0x1E)) >> 2;
            break;
        }
    }
    return (u32) var_r4;
}
