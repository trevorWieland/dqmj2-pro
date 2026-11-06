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
extern u32 native_fn_02061088();
extern u32 native_fn_0206256c();
extern u8 native_data_020dac90[];
u32 native_main_02061950(s32 arg0) {
    s8 var_r5;
    u32 (*temp_r4)();

    var_r5 = 0;
    do {
        native_fn_02061088(arg0, 0, var_r5);
        var_r5 += 1;
    } while ((s32) var_r5 < 2);
    temp_r4 = *(u32 *)(native_data_020dac90 + (arg0 * 0xC));
    if (temp_r4 == NULL) {
        return (u32) native_data_020dac90;
    }
    native_fn_0206256c(0x900);
    return temp_r4();
}
