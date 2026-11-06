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
extern u32 native_fn_02048034();
extern u32 native_fn_02062a10();
extern u32 native_fn_020633b0();
extern u32 native_fn_020bb1f8();
extern u8 native_data_01fffab0[];
u32 native_itcm_01ffc714(void) {
    u32 var_r0;
    u8 *var_r1;
    u32 temp_r4;
    s32 var_r5;

    temp_r4 = native_fn_020633b0();
    if (native_fn_020bb1f8() == 0) {
        return -2U;
    }
    var_r1 = native_data_01fffab0;
    var_r5 = 0;
loop_3:
    if ((s8) *var_r1 != 0) {
        if (var_r5 < 3) {
            var_r0 = native_fn_02062a10(M2C_FIELD((temp_r4 + (var_r5 * 4)), s32 *, 0x1C));
        } else {
            var_r0 = native_fn_02062a10(M2C_FIELD((temp_r4 + ((var_r5 - 3) * 4)), s32 *, 0x28));
        }
        native_fn_02048034(var_r0, 0);
        return (u32) var_r5;
    }
    var_r5 = (s32) (s8) (var_r5 + 1);
    var_r1 += 1;
    if (var_r5 >= 6) {
        return -1U;
    }
    goto loop_3;
}
