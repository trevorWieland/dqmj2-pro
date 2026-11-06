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
extern u32 native_fn_0201d984();
extern u32 native_fn_0201f274();
extern u32 native_fn_020b3250();
extern u32 native_fn_020b32c4();
extern u32 native_fn_020b35dc();
extern u8 native_data_020e165c[];
extern u8 native_data_020e166c[];
extern u8 native_data_020e1680[];
extern u8 native_data_020e1688[];
extern u8 native_data_020e168c[];
extern u8 native_data_020e1690[];
extern u8 native_data_020e1698[];
u32 native_main_020b33ec(u32 arg0) {
    u32 sp4;
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r4;
    u32 temp_r6;
    u32 temp_r7;
    u32 var_r0;
    u32 var_r4;
    u8 *var_r3;

    native_fn_020b3250(arg0, native_data_020e1680);
    sp4 = native_fn_0201f274();
    native_fn_020b3250(arg0, native_data_020e166c);
    temp_r4 = native_fn_0201f274();
    native_fn_020b3250(arg0, native_data_020e1688);
    temp_r6 = native_fn_0201f274();
    native_fn_020b3250(arg0, native_data_020e168c);
    temp_r7 = native_fn_0201f274();
    temp_r0 = native_fn_020b32c4(1, temp_r4, temp_r6);
    var_r0 = -1U;
    if (temp_r0 != -1U) {
        native_fn_020b3250(arg0, native_data_020e1690);
        var_r4 = native_fn_0201f274();
        temp_r0_2 = native_fn_0201d984(arg0, native_data_020e1698);
        if (temp_r0_2 == 0) {
            var_r4 = 0;
            var_r3 = native_data_020e165c;
        } else {
            var_r3 = temp_r0_2 + 6;
        }
        var_r0 = native_fn_020b35dc(temp_r0, sp4, temp_r7, var_r3, var_r4);
    }
    return var_r0;
}
