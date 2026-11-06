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
extern u32 native_fn_02026144();
u32 native_ov000_021edfdc(void *arg0, s32 arg1) {
    u16 temp_r0_2;
    u16 temp_r4;
    u32 temp_r0;

    temp_r0_2 = M2C_FIELD(arg0, u16 *, 0xE);
    if (temp_r0_2 == 0) {
        return (u32) temp_r0_2;
    }
    if ((s32) temp_r0_2 <= arg1) {
        M2C_FIELD(arg0, s32 *, 0) = (s32) (temp_r0_2 - 1);
    } else {
        M2C_FIELD(arg0, s32 *, 0) = arg1;
    }
    temp_r4 = M2C_FIELD(arg0, u16 *, 0xC);
    temp_r0 = temp_r4 * native_fn_02026144(M2C_FIELD(arg0, s32 *, 0), temp_r4);
    M2C_FIELD(arg0, u32 *, 4) = temp_r0;
    return temp_r0;
}
