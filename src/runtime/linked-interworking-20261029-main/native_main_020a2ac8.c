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
extern u32 native_fn_02008c14();
extern u32 native_fn_0209aa64();
extern u8 native_data_021d1ba8[];
u32 native_main_020a2ac8(void) {
    s32 temp_r1;
    s32 var_r4;
    u8 *var_r5;

    var_r4 = 0;
    var_r5 = native_data_021d1ba8;
    do {
        temp_r1 = M2C_FIELD(var_r5, s32 *, 4);
        if (temp_r1 != 0) {
            native_fn_0209aa64(4, temp_r1, 0);
        }
        var_r4 += 1;
        var_r5 += 0xC;
    } while (var_r4 < 0x9A);
    return native_fn_02008c14(0, native_data_021d1ba8, 0x738);
}
