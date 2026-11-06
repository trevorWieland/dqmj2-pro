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
extern u32 native_fn_0207afec();
extern u32 native_fn_0207b004();
extern u32 native_fn_0207b02c();
extern u32 native_fn_ov001_021dd02c();
extern u32 native_fn_ov001_021e2c60();
extern u32 native_fn_ov001_021f73b8();
u32 native_ov001_021fcb64(void *arg0, s32 arg1) {
    u32 var_r4;

    var_r4 = 1;
    if (native_fn_ov001_021dd02c(arg0, arg1, native_fn_0207b02c(arg1, 0x80000400)) == 0) {
        var_r4 = 0;
    } else if ((arg1 == 0xDF) && (native_fn_ov001_021f73b8(0) == 0)) {
        var_r4 = 0;
    } else if ((native_fn_0207b02c(arg1, 0x80000200) != 0) && ((s32) M2C_FIELD(arg0, s8 *, 0x234) < 3)) {
        var_r4 = 0;
    } else if (native_fn_ov001_021e2c60(M2C_FIELD(arg0, u8 *, 0x31E), M2C_FIELD(arg0, u8 *, 0x31F), arg1) != 0) {
        var_r4 = 0;
    } else if ((M2C_FIELD(arg0, s8 *, 0x23C) != 0) && (native_fn_0207b004(arg1, 2) != 0)) {
        var_r4 = 0;
    } else if ((M2C_FIELD(arg0, s8 *, 0x23E) != 0) && (native_fn_0207b004(arg1, 8) != 0)) {
        var_r4 = 0;
    } else if ((M2C_FIELD(arg0, s8 *, 0x254) != 0) && (native_fn_0207b004(arg1, 0x04000000) != 0)) {
        var_r4 = 0;
    } else if ((M2C_FIELD(arg0, s8 *, 0x23D) != 0) && (native_fn_0207b004(arg1, 4) != 0)) {
        var_r4 = 0;
    } else if ((M2C_FIELD(arg0, s8 *, 0x255) != 0) && (native_fn_0207b004(arg1, 0x02000000) != 0)) {
        var_r4 = 0;
    } else if ((M2C_FIELD(arg0, s8 *, 0x266) != 0) && (((u32) (M2C_FIELD((void *) native_fn_0207afec(arg1), u16 *, 8) << 0x14) >> 0x1C) == 4) && (M2C_FIELD((void *) native_fn_0207afec(arg1), u8 *, 0x21) == 0x2B)) {
        var_r4 = 0;
    }
    return var_r4;
}
