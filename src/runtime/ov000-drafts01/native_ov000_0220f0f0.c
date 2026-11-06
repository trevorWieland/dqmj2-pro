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
extern u32 native_fn_ov000_0220a2a4();
u32 native_ov000_0220f0f0(void *arg0) {
    u32 var_r5;
    u8 temp_r0;

    var_r5 = 0;
    if (M2C_FIELD(arg0, u8 *, 0x279) == 0) {
        native_fn_ov000_0220a2a4(arg0, 0, 0);
        M2C_FIELD(arg0, u8 *, 0x279) = 0xAU;
        if ((M2C_FIELD(arg0, u8 *, 0x1E2) != 0) && (M2C_FIELD(arg0, u8 *, 0x160) != 0)) {

        } else {
            M2C_FIELD(arg0, u8 *, 0x279) = 0x14U;
        }
    }
    temp_r0 = M2C_FIELD(arg0, u8 *, 0x279);
    if (temp_r0 == 0xA) {
        var_r5 = 1;
    }
    if (temp_r0 == 0x14) {
        var_r5 = 1;
        M2C_FIELD(arg0, u8 *, 0x1E2) = 0U;
    }
    return var_r5;
}
