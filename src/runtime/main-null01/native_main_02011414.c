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
extern u32 native_fn_02008430();
extern u32 native_fn_02011478();
extern u8 native_data_020e5d60[];
u32 native_main_02011414(u32 arg0, s32 arg1) {
    u32 var_r0;

    if ((arg1 & 0x3F) == 0x11) {
        if (M2C_FIELD(native_data_020e5d60, u32 *, 0) != 0) {
            return M2C_FIELD(native_data_020e5d60, u32 *, 0);
        }
        var_r0 = 1;
        M2C_FIELD(native_data_020e5d60, u32 *, 0) = 1U;
        if (M2C_FIELD(native_data_020e5d60, u32 (**)(), 4) != NULL) {
            var_r0 = M2C_FIELD(native_data_020e5d60, u32 (**)(), 4)();
        }
        if (var_r0 == 0) {
            return var_r0;
        }
        return native_fn_02011478();
    }
    return native_fn_02008430();
}
