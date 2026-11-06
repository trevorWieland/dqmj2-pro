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
extern u32 native_fn_0205c944();
extern u32 native_fn_0205cf5c();
extern u8 native_data_02102e2c[];
extern u8 native_data_021043ac[];
u32 native_main_0205d634(void) {
    u8 *var_r4;
    s32 var_r5;
    s32 var_r5_2;
    u32 var_r6;
    u8 *var_r7;

    var_r6 = 0;
    var_r7 = native_data_021043ac;
    var_r5 = 0;
    do {
        if (*var_r7 != 0) {
            native_fn_0205cf5c(var_r7);
            *var_r7 = 0;
        }
        var_r5 += 1;
        var_r7 += 0x11C;
    } while (var_r5 < 0x20);
    var_r4 = native_data_02102e2c;
    var_r5_2 = 0;
    do {
        if ((s32) M2C_FIELD(var_r4, s32 *, 4) > 0) {
            native_fn_0205c944(var_r4);
            var_r6 += 1;
        }
        var_r5_2 += 1;
        var_r4 += 0xAC;
    } while (var_r5_2 < 0x20);
    return var_r6;
}
