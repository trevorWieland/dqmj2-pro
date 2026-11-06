#define NULL ((void *)0)
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
extern u32 native_fn_020b2c88();
extern u8 native_data_020e041c[];
u32 native_main_020a9f88(s32 *arg0, s32 arg1, s32 arg2, s32 arg3) {
    void *temp_r1;
    s32 temp_r4;

    if ((arg0 == NULL) || (temp_r4 = *arg0, (temp_r4 == 0))) {
        return 2U;
    }
    if ((arg1 < 0) || (arg1 >= 9)) {
        native_fn_020b2c88(arg0, native_data_020e041c);
        return 2U;
    }
    temp_r1 = temp_r4 + (arg1 * 8);
    M2C_FIELD(temp_r1, s32 *, 0x1A8) = arg2;
    M2C_FIELD(temp_r1, s32 *, 0x1AC) = arg3;
    return 0U;
}
