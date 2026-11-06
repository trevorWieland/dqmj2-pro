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
extern u32 native_fn_02008d78();
extern u32 native_fn_020449d4();
extern u32 native_fn_020647c4();
u32 native_ov000_02227cec(void *arg0) {
    s32 var_r2;
    void *temp_r0;

    native_fn_020647c4(M2C_FIELD(arg0, s16 *, 0x18), M2C_FIELD(arg0, u8 *, 0x1A), arg0 + 0x20);
    M2C_FIELD(arg0, s16 *, 0x20) = (s16) (M2C_FIELD(arg0, s16 *, 0x20) * 2);
    if ((s32) M2C_FIELD(arg0, s16 *, 0x20) > (s32) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x10)) {
        M2C_FIELD(arg0, s16 *, 0x20) = (s16) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x10);
    }
    M2C_FIELD(arg0, s16 *, 0x22) = (s16) (M2C_FIELD(arg0, s16 *, 0x22) * 2);
    if ((s32) M2C_FIELD(arg0, s16 *, 0x22) > (s32) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x12)) {
        M2C_FIELD(arg0, s16 *, 0x22) = (s16) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x12);
    }
    M2C_FIELD(arg0, s16 *, 0x24) = (s16) M2C_FIELD(arg0, s16 *, 0x20);
    M2C_FIELD(arg0, s16 *, 0x26) = (s16) M2C_FIELD(arg0, s16 *, 0x22);
    M2C_FIELD(arg0, s16 *, 0x28) = (s16) (M2C_FIELD(arg0, s16 *, 0x28) * 2);
    if ((s32) M2C_FIELD(arg0, s16 *, 0x28) > (s32) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x14)) {
        M2C_FIELD(arg0, s16 *, 0x28) = (s16) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x14);
    }
    M2C_FIELD(arg0, s16 *, 0x2A) = (s16) (M2C_FIELD(arg0, s16 *, 0x2A) * 2);
    if ((s32) M2C_FIELD(arg0, s16 *, 0x2A) > (s32) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x16)) {
        M2C_FIELD(arg0, s16 *, 0x2A) = (s16) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x16);
    }
    M2C_FIELD(arg0, s16 *, 0x2C) = (s16) (M2C_FIELD(arg0, s16 *, 0x2C) * 2);
    if ((s32) M2C_FIELD(arg0, s16 *, 0x2C) > (s32) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x18)) {
        M2C_FIELD(arg0, s16 *, 0x2C) = (s16) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x18);
    }
    M2C_FIELD(arg0, s16 *, 0x2E) = (s16) (M2C_FIELD(arg0, s16 *, 0x2E) * 2);
    if ((s32) M2C_FIELD(arg0, s16 *, 0x2E) > (s32) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x1A)) {
        M2C_FIELD(arg0, s16 *, 0x2E) = (s16) M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD(arg0, s16 *, 0x18)), u16 *, 0x1A);
    }
    var_r2 = 0;
    do {
        temp_r0 = arg0 + (var_r2 * 2);
        var_r2 += 1;
        M2C_FIELD(temp_r0, s8 *, 0x7B) = 0;
    } while (var_r2 < 5);
    M2C_FIELD(arg0, s8 *, 0x1C) = 0;
    M2C_FIELD(arg0, s8 *, 0x1E) = 0;
    return native_fn_02008d78(arg0 + 0x40, 0, 0x3A);
}
