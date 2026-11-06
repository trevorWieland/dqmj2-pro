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
extern u32 native_fn_0205f98c();
u32 native_ov001_022066b0(void *arg0) {
    u8 var_r6;
    void *temp_r0;

    M2C_FIELD(arg0, s8 *, 0x23) = 1;
    var_r6 = 0;
    M2C_FIELD(arg0, s16 *, 0x26) = 0xF;
    M2C_FIELD(arg0, s32 *, 0x30) = 0;
    do {
        temp_r0 = (void *) native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), 0);
        M2C_FIELD(temp_r0, s32 *, 0x7C) = (s32) (M2C_FIELD(temp_r0, s32 *, 0x7C) & ~2);
        var_r6 += 1;
    } while ((u32) var_r6 < 4U);
    return (u32) temp_r0;
}
