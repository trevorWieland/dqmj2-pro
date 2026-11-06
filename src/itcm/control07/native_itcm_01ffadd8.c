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
extern u32 native_fn_02048f6c();
extern u32 native_fn_02049898(u32);
extern u32 native_fn_02049ad0();
extern u32 native_fn_020897ec();
extern u32 native_fn_ov000_02223c04();
extern u32 native_fn_ov000_02223c14();
u32 native_itcm_01ffadd8(void) {
    s8 var_r4;
    u32 value;
    u32 temp_r4;

    var_r4 = 4;
    do {
        value = native_fn_02049ad0(var_r4);
        if (*(s32 *)value != 0) {
            native_fn_02049898(value);
        }
        var_r4 += 1;
    } while ((s32) var_r4 <= 0xC);
    temp_r4 = native_fn_02048f6c(1);
    native_fn_ov000_02223c04((s8) temp_r4, native_fn_ov000_02223c14((s8) native_fn_02048f6c(1)));
    return native_fn_020897ec(0);
}
