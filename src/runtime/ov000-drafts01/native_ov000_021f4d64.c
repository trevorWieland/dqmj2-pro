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
extern u32 native_fn_02061944();
extern u32 native_fn_ov000_021f4dac();
u32 native_ov000_021f4d64(void) {
    u32 temp_r4;
    u32 var_r5;

    temp_r4 = native_fn_02061944();
    var_r5 = 0;
    native_fn_ov000_021f4dac();
    if (M2C_FIELD(temp_r4, s8 *, 0x26C) != 0x2A) {
        var_r5 = 1;
    }
    return var_r5;
}
