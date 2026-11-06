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
extern u8 native_data_ov000_0223526c[];
u32 native_ov000_021e8e1c(s32 arg0, u32 arg1) {
    s32 temp_r3;
    u32 var_r0;

    temp_r3 = (arg0 * 0x2CC) + (s32) native_data_ov000_0223526c;
    var_r0 = 0;
    if (M2C_FIELD(temp_r3, u8 *, 0x274) != 0) {
        var_r0 = M2C_FIELD(temp_r3, u32 *, 0x29C);
        M2C_FIELD(temp_r3, u32 *, 0x29C) = arg1;
    }
    return var_r0;
}
