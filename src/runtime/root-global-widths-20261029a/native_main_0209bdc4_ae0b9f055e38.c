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
extern u32 native_fn_0209bd20();
extern u32 native_fn_0209bd6c();
extern u32 native_fn_0209bdb8();
extern u8 native_data_021d19e0[];
u32 native_main_0209bdc4(s32 arg0, s32 arg1) {
    u8 var_r2;

    var_r2 = 0;
    if (arg1 > 0) {
loop_2:
        if (arg0 != M2C_FIELD((*(u32 *)native_data_021d19e0 + (var_r2 * 4)), s32 *, 0x46C)) {
            var_r2 += 1;
            if ((s32) var_r2 < arg1) {
                goto loop_2;
            }
        }
    }
    if ((s32) var_r2 >= arg1) {
        return 0U;
    }
    native_fn_0209bd20(M2C_FIELD((*(u32 *)native_data_021d19e0 + var_r2), u8 *, 0x648));
    native_fn_0209bd6c();
    return native_fn_0209bdb8();
}
