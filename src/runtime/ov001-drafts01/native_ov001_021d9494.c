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
extern u32 native_fn_020430b4();
u32 native_ov001_021d9494(void *arg0, s8 arg1, u32 arg2) {
    u32 temp_r0;

    temp_r0 = native_fn_02042464(arg0, M2C_FIELD((native_fn_020430b4(M2C_FIELD(arg0, s16 *, 0x16A)) + (arg1 * 2)), s16 *, 4), arg2);
    M2C_FIELD(arg0, s8 *, 0x1E4) = arg1;
    return temp_r0;
}
