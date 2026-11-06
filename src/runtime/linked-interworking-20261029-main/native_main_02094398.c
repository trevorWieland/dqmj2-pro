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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_02094730();
extern u32 native_fn_0209477c();
extern u32 native_fn_02094824();
extern u32 native_fn_02094848();
extern u32 native_fn_02094d70();
extern u32 native_fn_02095280();
extern u32 native_fn_020956dc();
extern u32 native_fn_02095778();
extern u32 native_fn_02095d50();
extern u32 native_fn_02095da8();
u32 native_main_02094398(void) {
    u32 temp_r4;
    u32 temp_r4_2;
    u32 var_r5;

    var_r5 = native_fn_0209477c();
    if (var_r5 == 1) {
        var_r5 = native_fn_02095d50();
    } else if (var_r5 < 7U) {
        temp_r4_2 = native_fn_02007ff4();
        var_r5 = native_fn_02095778();
        native_fn_02094730();
        native_fn_02008008(temp_r4_2);
    } else if (var_r5 < 9U) {
        var_r5 = native_fn_02094d70();
    } else if (var_r5 < 0xAU) {
        var_r5 = native_fn_020956dc();
    } else if (var_r5 < 0x10U) {
        var_r5 = native_fn_02095da8();
    } else if (var_r5 == 0x11) {
        var_r5 = native_fn_02095280();
    }
    native_fn_02094730(var_r5);
    if (var_r5 == 0x10) {
        temp_r4 = native_fn_02094848();
        native_fn_02094824();
        return temp_r4;
    }
    if (var_r5 == 0x12) {
        native_fn_02094824();
        return -1U;
    }
    return 0U;
}
