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
extern u32 native_fn_020c56b4();
u32 native_ov000_0221008c(void *arg0) {
    u32 var_r4;
    u8 temp_r0;

    temp_r0 = M2C_FIELD(arg0, u8 *, 0x278);
    var_r4 = 1;
    if (temp_r0 == 8) {
        var_r4 = 0;
    } else if (temp_r0 == 9) {
        var_r4 = 0;
    } else if (temp_r0 == 1) {
        var_r4 = 0;
    } else if ((temp_r0 == 5) && (M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 9) == 3)) {
        var_r4 = 0;
    } else if ((M2C_FIELD(arg0, u8 *, 0x278) == 6) && (M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 8) == 3)) {
        var_r4 = 0;
    } else if ((M2C_FIELD(arg0, u8 *, 0x278) == 3) && (M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 7) == 8)) {
        var_r4 = 0;
    } else if ((M2C_FIELD(arg0, u8 *, 0x278) == 5) && (M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 9) == 5)) {
        var_r4 = 0;
    } else if (((M2C_FIELD(arg0, u8 *, 0x278) == 3) && (M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 7) == 7)) || ((M2C_FIELD(arg0, u8 *, 0x278) == 3) && (M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 7) == 9))) {
        var_r4 = 0;
    } else if (M2C_FIELD(arg0, u8 *, 0x1E4) == 2) {
        var_r4 = 0;
    }
    return var_r4;
}
