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
extern u32 native_fn_ov000_02215cb4();
u32 native_ov000_02215ce4(u32 arg0, u32 arg1) {
    u16 temp_r2;
    u32 temp_r1;
    void *temp_r0;

    if (native_fn_ov000_02215cb4() == 0) {
        return 0U;
    }
    temp_r0 = (void *) native_fn_0207afec(arg1);
    temp_r2 = M2C_FIELD(temp_r0, u16 *, 8);
    if (((u32) (temp_r2 << 0x18) >> 0x1C) != 0) {
        return 0U;
    }
    if (((u32) (temp_r2 << 0x1C) >> 0x1C) != 6) {
        return 0U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1E) != 1) {
        return 0U;
    }
    temp_r1 = (u32) (temp_r2 << 0x14) >> 0x1C;
    if ((temp_r1 != 2) && (temp_r1 != 3)) {
        return 0U;
    }
    if ((u32) (u16) (s16) (M2C_FIELD(temp_r0, s16 *, 6) + 0xFFFFD8F0) <= 1U) {
        return 0U;
    }
    if (M2C_FIELD(temp_r0, s16 *, 0x10) != 0) {
        return 1U;
    }
    return 0U;
}
