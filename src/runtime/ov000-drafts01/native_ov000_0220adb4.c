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
extern u32 native_fn_02041f34();
extern u32 native_fn_02042c0c();
extern u32 native_fn_020c56b4();
extern u32 native_fn_ov000_0220a2a4();
u32 native_ov000_0220adb4(void *arg0) {
    if (M2C_FIELD(arg0, u8 *, 0x279) != 0) {
        return (u32) arg0;
    }
    native_fn_ov000_0220a2a4(arg0, 0, 0);
    native_fn_02041f34(arg0, M2C_FIELD(arg0, s32 *, 0x2A8), M2C_FIELD(arg0, s32 *, 0x2AC), M2C_FIELD(arg0, s32 *, 0x2B0));
    if ((M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 6) == 3) || (M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 6) == 4)) {
        native_fn_02042c0c(arg0, 0x1F);
    } else {
        native_fn_02042c0c(arg0, 0);
    }
    M2C_FIELD(arg0, u8 *, 0x279) = 0xAU;
    return 0xAU;
}
