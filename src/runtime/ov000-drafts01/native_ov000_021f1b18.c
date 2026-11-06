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
extern u32 native_fn_ov000_021f35b0();
u32 native_ov000_021f1b18(u16 *arg0, u16 *arg1) {
    s32 var_r0;
    u8 temp_r0;
    u8 temp_r4;

    temp_r4 = *(u8 *) native_fn_ov000_021f35b0(*arg0);
    temp_r0 = *(u8 *) native_fn_ov000_021f35b0(*arg1);
    if ((u32) temp_r4 > (u32) temp_r0) {
        return 1U;
    }
    if ((u32) temp_r4 < (u32) temp_r0) {
        var_r0 = 1;
    } else {
        var_r0 = 0;
    }
    return 0 - var_r0;
}
