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
extern u32 native_fn_0205bf4c();
extern u32 native_fn_0205bf5c();
extern u32 native_fn_ov000_021da08c();
extern u32 native_fn_ov000_021df1d0();
extern u32 native_fn_ov000_021e0f58();
extern u8 native_data_020dd8e8[];
u32 native_main_0203fe08(void) {
    u32 temp_r0;
    u32 var_r0;
    u32 var_r4;

    var_r0 = native_fn_ov000_021df1d0();
    if (var_r0 != 0) {
        var_r0 = (u32) M2C_FIELD(native_data_020dd8e8, s8 *, 1);
        if (var_r0 != 0) {
            temp_r0 = native_fn_ov000_021e0f58();
            if (temp_r0 == 0) {
                return temp_r0;
            }
            var_r4 = native_fn_0205bf4c() + 1;
            if (var_r4 > 0x4650U) {
                var_r4 = 0;
            }
            native_fn_ov000_021da08c(var_r4);
            return native_fn_0205bf5c(var_r4);
        }
    }
    return var_r0;
}
