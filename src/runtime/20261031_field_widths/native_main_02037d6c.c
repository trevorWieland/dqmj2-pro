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
extern u32 native_fn_0202b784(u32, u32, u32);
extern u32 native_fn_0202ba20(void *, u32);
extern u32 native_fn_02037d28(u32);
u32 native_main_02037d6c(s32 *arg0) {
    u32 temp_r0;

    temp_r0 = native_fn_0202b784(*arg0, 0x14, 4);
    if (temp_r0 == 0) {
        return 0U;
    }
    native_fn_02037d28(temp_r0);
    native_fn_0202ba20((u8 *)arg0 + 4, temp_r0);
    return 1U;
}
