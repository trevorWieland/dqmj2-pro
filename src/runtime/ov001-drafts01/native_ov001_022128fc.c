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
extern u32 native_fn_02048a60();
extern u32 native_fn_0205f98c();
u32 native_ov001_022128fc(void *arg0) {
    s16 temp_r1;
    s16 temp_r2;
    s32 var_r1;
    void *temp_r0;

    M2C_FIELD(arg0, s16 *, 0x26) = (s16) (M2C_FIELD(arg0, s16 *, 0x26) - 2);
    temp_r0 = (void *) native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), 0);
    temp_r2 = M2C_FIELD(temp_r0, s16 *, 0x8E);
    if ((s32) temp_r2 > 0) {
        if ((s32) M2C_FIELD(arg0, s16 *, 0x1A) >= 0) {
            M2C_FIELD(arg0, s16 *, 0x1A) = (s16) (0 - temp_r2);
        } else {
            M2C_FIELD(arg0, s16 *, 0x1A) = temp_r2;
            M2C_FIELD(temp_r0, s16 *, 0x8E) = (s16) (M2C_FIELD(temp_r0, s16 *, 0x8E) - 1);
        }
        temp_r1 = M2C_FIELD(temp_r0, s16 *, 0x8E);
        var_r1 = temp_r1 >> 1;
        if (temp_r1 & 1) {
            var_r1 = 0 - var_r1;
        }
        M2C_FIELD(arg0, s16 *, 0x18) = (s16) var_r1;
    }
    native_fn_02048a60(temp_r0, M2C_FIELD(arg0, s16 *, 0x14) + M2C_FIELD(arg0, s16 *, 0x18), M2C_FIELD(arg0, s16 *, 0x16) + M2C_FIELD(arg0, s16 *, 0x1A));
    if ((s32) M2C_FIELD(arg0, s16 *, 0x26) < 0) {
        return 1U;
    }
    return 0U;
}
