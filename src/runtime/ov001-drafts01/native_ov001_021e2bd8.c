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
extern u32 native_fn_02044414();
extern u32 native_fn_02044424();
extern u32 native_fn_ov001_021e2bbc();
u32 native_ov001_021e2bd8(void) {
    s32 var_r0;
    s32 var_r4;

    if (native_fn_ov001_021e2bbc() == 0) {
        return -1U;
    }
    if (native_fn_02044424(0x800000) != 0) {
        var_r4 = 5;
    } else {
        var_r4 = 0xA;
    }
    var_r0 = var_r4 - native_fn_02044414();
    if (var_r0 < 0) {
        var_r0 = 0;
    }
    return (u32) var_r0;
}
