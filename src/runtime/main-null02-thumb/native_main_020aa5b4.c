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
extern u32 native_fn_020ac4a8();
extern u32 native_fn_020b2c88();
extern u8 native_data_020e0440[];
u32 native_main_020aa5b4(void **arg0, u32 arg1) {
    u32 var_r0;
    void *temp_r4;

    if ((arg0 == NULL) || (temp_r4 = *arg0, (temp_r4 == NULL))) {
        return 2U;
    }
    if (M2C_FIELD(temp_r4, s32 *, 0x108) != 0) {
        return 0U;
    }
    if (M2C_FIELD(temp_r4, s32 *, 0x1F4) == 4) {
        native_fn_020b2c88(arg0, native_data_020e0440);
        return 2U;
    }
    var_r0 = native_fn_020ac4a8(arg0, arg1, 1);
    if (var_r0 == 0) {
        var_r0 = 0;
    }
    return var_r0;
}
