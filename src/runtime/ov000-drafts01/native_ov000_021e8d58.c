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
extern u32 native_fn_02042464();
extern u8 native_data_ov000_0223526c[];
u32 native_ov000_021e8d58(s32 arg0, u32 arg1, s8 arg2) {
    s32 temp_r0;

    temp_r0 = (0x2CC * arg0) + (s32) native_data_ov000_0223526c;
    if (M2C_FIELD(temp_r0, u8 *, 0x274) == 0) {
        return 0U;
    }
    M2C_FIELD(temp_r0, s8 *, 0x275) = -1;
    M2C_FIELD(temp_r0, s8 *, 0x15F) = arg2;
    native_fn_02042464(temp_r0, arg1, 0);
    return 1U;
}
