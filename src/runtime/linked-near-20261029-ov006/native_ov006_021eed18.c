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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02008c28();
extern u32 native_fn_0208b190();
extern u32 native_fn_0208b1cc();
extern u32 native_fn_0208b224();
u32 native_ov006_021eed18(s32 arg0, s32 arg1) {
    s32 temp_r0;
    s32 var_r4;
    s32 var_r5;

    var_r5 = arg0;
    native_fn_0208b1cc(1);
    temp_r0 = (s32) native_fn_0208b190();
    if (temp_r0 > 0) {
        var_r4 = 0;
        if (temp_r0 > 0) {
loop_2:
            if (var_r4 < arg1) {
                native_fn_02008c28(native_fn_0208b224((u16) var_r4), var_r5, 0xC0);
                var_r4 += 1;
                var_r5 += 0xC0;
                if (var_r4 < temp_r0) {
                    goto loop_2;
                }
            }
        }
    }
    native_fn_0208b1cc(0);
    return (u32) temp_r0;
}
