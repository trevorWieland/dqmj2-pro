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
extern u32 native_fn_02044fcc();
extern u32 native_fn_02063520();
u32 native_main_0206434c(void) {
    s32 var_r5;
    s32 var_r6;
    u16 var_r7;

    var_r7 = 0;
    var_r5 = 0;
    do {
        var_r6 = 0;
loop_2:
        if ((native_fn_02044fcc(var_r6, var_r5) == 0) && (native_fn_02063520(var_r6, var_r5) != 0)) {
            var_r7 += 1;
        }
        var_r6 += 1;
        if (var_r6 < 0x200) {
            goto loop_2;
        }
        var_r5 += 1;
    } while (var_r5 < 3);
    return (u32) var_r7;
}
