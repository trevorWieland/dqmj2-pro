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
extern u32 native_fn_02008064();
extern u32 native_fn_02008430();
extern u32 native_fn_0200877c();
extern u32 native_fn_0200ea38();
extern u32 native_fn_02011564();
u32 native_main_02011478(void) {
    s32 var_r5;
    u32 var_r0;

    var_r5 = 1;
    native_fn_0200877c(0);
    native_fn_0200877c(1);
    native_fn_0200877c(2);
    native_fn_0200877c(3);
    if (((s32) (*(u16 *)0x027FFFA8 & 0x8000) >> 0xF) != 0) {
        var_r0 = native_fn_0200ea38();
        if (var_r0 == 4) {
            do {
                native_fn_02008064(0xA3A47);
                var_r0 = native_fn_0200ea38();
            } while (var_r0 == 4);
        }
        if (var_r0 == 0) {
            var_r5 = 0;
        }
    }
    if (var_r5 != 0) {
        native_fn_02011564(1, 1);
    }
    return native_fn_02008430();
}
