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
extern u32 native_fn_02082e10();
extern u32 native_fn_02083504();
u32 native_main_02084434(s32 arg0) {
    u32 var_r4;

    var_r4 = 0;
    if (native_fn_02083504() == 2) {
        if ((native_fn_02082e10() != 0) && (arg0 != 0)) {
            do {

            } while (native_fn_02083504() != 1);
            var_r4 = 1;
        }
    }
    return var_r4;
}
