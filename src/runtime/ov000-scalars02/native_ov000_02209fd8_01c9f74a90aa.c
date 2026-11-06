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
extern u32 native_fn_ov000_02209dac();
extern u8 native_data_ov000_0223879e[];
u32 native_ov000_02209fd8(u32 arg0, s32 arg1, u32 arg2, u32 arg3, s32 arg4, s32 arg5, s32 arg6, u8 arg7, u8 arg8) {
    s32 temp_r0;

    temp_r0 = (s32) native_fn_ov000_02209dac(arg0, arg2, arg3, arg4, arg5, arg6, (s32) arg7, (s32) arg8);
    if (temp_r0 < 0) {
        return (u32) temp_r0;
    }
    *(u16 *)(native_data_ov000_0223879e + (temp_r0 * 0x2C4)) = arg1 + 0x34;
    return (u32) temp_r0;
}
