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
extern u32 native_fn_02042104();
extern u32 native_fn_0205cba4();
extern u32 native_fn_020c56b4();
extern u32 native_fn_ov000_021e7b9c();
extern u32 native_fn_ov000_0220c598();
u32 native_ov000_0220c5cc(void *arg0) {
    u32 var_r4;

    var_r4 = 0;
    if ((M2C_FIELD(arg0, u8 *, 0x1E2) == 0) || ((u32) M2C_FIELD(arg0, u8 *, 0x160) <= 0xAU)) {
        M2C_FIELD(arg0, u8 *, 0x279) = 0x14U;
    }
    if (M2C_FIELD(arg0, u8 *, 0x279) == 0) {
        native_fn_0205cba4(6, arg0, 1);
        native_fn_ov000_021e7b9c(0x92);
        if ((M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 9) == 4) || (M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 8) == 7)) {
            var_r4 = 1;
        } else {
            M2C_FIELD(arg0, s32 *, 0x27C) = (s32) ((s32) native_fn_ov000_0220c598(arg0) >> 3);
            M2C_FIELD(arg0, s16 *, 0x27A) = 0;
            M2C_FIELD(arg0, u8 *, 0x279) = 0xAU;
        }
    }
    if (M2C_FIELD(arg0, u8 *, 0x279) == 0xA) {
        native_fn_02042104(arg0, M2C_FIELD(arg0, s32 *, 0x27C), 0);
        M2C_FIELD(arg0, s16 *, 0x27A) = (s16) (M2C_FIELD(arg0, s16 *, 0x27A) + 1);
        if ((s32) M2C_FIELD(arg0, s16 *, 0x27A) >= 8) {
            M2C_FIELD(arg0, u8 *, 0x279) = 0x14U;
        }
    }
    if (M2C_FIELD(arg0, u8 *, 0x279) == 0x14) {
        var_r4 = 1;
    }
    return var_r4;
}
