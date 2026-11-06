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
extern u32 native_fn_0201d444();
extern u32 native_fn_02040884();
extern u32 native_fn_02040dc0();
extern u32 native_fn_0204199c();
extern u32 native_fn_02042f8c();
extern u8 native_data_020dd948[];
extern u8 native_data_020dd954[];
extern u8 native_data_020f621c[];
u32 native_main_020419b4(u32 arg0) {
    u8 sp0[16];
    u32 temp_r0;
    u32 var_r5;

    var_r5 = 0;
    if (arg0 < 0x1DDU) {
        if (native_fn_0204199c() == 0) {
            temp_r0 = native_fn_02040884(arg0, native_data_020f621c, 0xA);
            if (temp_r0 != 0) {
                native_fn_0201d444(&sp0, native_data_020dd948, native_fn_02042f8c(arg0));
                var_r5 = native_fn_02040dc0(temp_r0, native_data_020dd954, &sp0, 1);
            }
        } else {
            var_r5 = 1;
        }
    }
    return var_r5;
}
