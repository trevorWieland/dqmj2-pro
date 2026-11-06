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
extern u32 native_fn_02008d78();
extern u32 native_fn_020bf61c();
extern u32 native_fn_020bf76c();
extern u32 native_fn_020bf990();
extern u8 native_data_021d4bec[];
u32 native_main_020bfb10(s32 arg0) {
    s32 var_r6;
    s32 var_r7;
    u32 temp_r5;
    u32 var_r0;

    var_r7 = 0;
    if (arg0 != 0) {
        var_r7 = 1;
    }
    native_fn_02008d78(M2C_FIELD(native_data_021d4bec, s32 *, 8), 0, 0x320);
    var_r6 = 0;
    do {
        var_r0 = native_fn_020bf76c(var_r6);
        temp_r5 = var_r0;
        if (temp_r5 != 0) {
            var_r0 = native_fn_020bf61c();
            if (var_r0 != 0) {
                if (temp_r5 != arg0) {
                    var_r0 = native_fn_020bf990(temp_r5, var_r7);
                    var_r7 += 1;
                } else {
                    var_r0 = native_fn_020bf990(temp_r5, 0);
                }
            }
        }
        var_r6 += 1;
    } while (var_r6 < 0x65);
    return var_r0;
}
