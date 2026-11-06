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
extern u32 native_fn_02041510();
extern u32 native_fn_02041800();
extern u32 native_fn_020418e8();
extern u32 native_fn_02081cac();
extern u8 native_data_020de5a4[];
extern u8 native_data_021c6e78[];
u32 native_main_0208232c(void) {
    u32 var_r4;

    var_r4 = 0;
    if ((s8) *native_data_021c6e78 != 0) {
        native_fn_02041510(0, 2, 5);
        native_fn_020418e8(5, 0xA);
        *native_data_021c6e78 = 0;
    }
    if (native_fn_02041800() == 1) {
        return 0U;
    }
    if ((s32) (s8) *native_data_020de5a4 >= 0) {
        *native_data_020de5a4 = (s8) *native_data_020de5a4 - 2;
        if ((s32) (s8) *native_data_020de5a4 <= 0) {
            *native_data_020de5a4 = 0;
            var_r4 = 1;
        }
    } else {
        var_r4 = 1;
    }
    native_fn_02081cac();
    return var_r4;
}
