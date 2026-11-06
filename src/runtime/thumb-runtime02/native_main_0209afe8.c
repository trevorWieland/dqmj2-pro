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
extern u32 native_fn_0208a268();
extern u32 native_fn_0209446c();
extern u32 native_fn_0209a9f8();
extern u32 native_fn_0209ac5c();
extern u32 native_fn_0209aee0();
u32 native_main_0209afe8(void) {
    u32 var_r4;

    native_fn_0209ac5c();
    if (native_fn_0209aee0() != 0) {
        var_r4 = native_fn_0209446c();
        if ((var_r4 == 0xFF) || (var_r4 > 0x63U)) {
            var_r4 = 0x63;
        }
        if (native_fn_0208a268() == 0xB) {
            native_fn_0209a9f8(9, 0xFFFF298C - var_r4);
        } else {
            native_fn_0209a9f8(8, 0xFFFF2D10 - var_r4);
        }
        return 1U;
    }
    return 0U;
}
