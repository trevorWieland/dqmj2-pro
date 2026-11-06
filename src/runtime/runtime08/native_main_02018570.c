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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_02016dc4();
extern u32 native_fn_0201852c();
extern u32 native_fn_02018564();
extern u32 native_fn_02018c94();
extern u32 native_fn_02018e40();
extern u8 native_data_020ec360[];
u32 native_main_02018570(void) {
    u32 temp_r4;
    u32 var_r5;

    var_r5 = 1;
    temp_r4 = native_fn_02007ff4();
    if (M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), u8 *, 0x50D) == 0) {
        native_fn_02016dc4(0);
    } else if (M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), u16 *, 0x526) == 0) {
        M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s32 *, 0x5E4) = 0;
        M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), u16 *, 0x526) = 1U;
        if (native_fn_02018c94() != 0) {
            native_fn_02018e40(native_fn_02018564);
            var_r5 = 0;
        } else {
            var_r5 = native_fn_0201852c();
        }
    }
    native_fn_02008008(temp_r4);
    return var_r5;
}
