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
extern u32 native_fn_0207c634();
extern u32 native_fn_ov001_021dbc18();
u32 native_ov001_021dbdfc(void *arg0) {
    s16 temp_r4;
    u32 var_r0;
    u32 var_r1;

    temp_r4 = M2C_FIELD(arg0, s16 *, 0x224);
    var_r0 = native_fn_ov001_021dbc18(arg0, 3, temp_r4 + native_fn_0207c634(arg0 + 0x1EC, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46));
    var_r1 = 0x270F;
    if ((s32) var_r0 < 0x270F) {
        var_r1 = var_r0;
    }
    if ((s32) var_r1 < 1) {
        return 1U;
    }
    if ((s32) var_r0 >= 0x270F) {
        var_r0 = 0x270F;
    }
    return var_r0;
}
