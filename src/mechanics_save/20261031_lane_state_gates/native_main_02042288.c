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
extern u32 native_fn_02028dac(void *);
extern u32 native_fn_0204124c(void *);
u32 native_main_02042288(void *arg0) {
    u32 temp_r0;

    if (M2C_FIELD(arg0, u8 *, 0x15C) != 0) {
        native_fn_0204124c(arg0);
        temp_r0 = native_fn_02028dac(arg0);
        if (temp_r0 != 0) {
            M2C_FIELD(arg0, u8 *, 0x15C) = 0U;
        }
        return temp_r0;
    }
    return 0U;
}
