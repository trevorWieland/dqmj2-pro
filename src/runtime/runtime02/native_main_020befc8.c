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
extern u8 native_data_021d423c[];
extern u8 native_data_021d44b4[];
u32 native_main_020befc8(void) {
    s32 var_r6;
    u8 *var_r7;

    var_r6 = 0;
    var_r7 = native_data_021d44b4;
    do {
        native_fn_02008d78(var_r7, 0, 0x268);
        var_r6 += 1;
        var_r7 += 0x268;
    } while (var_r6 < 3);
    M2C_FIELD(native_data_021d423c, s8 *, 1) = 0;
    return (u32) native_data_021d423c;
}
