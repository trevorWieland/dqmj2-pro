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
extern u32 native_fn_0205cf5c();
extern u32 native_fn_0205cfd4();
extern u32 native_fn_0205d068();
extern u32 native_fn_0205d25c();
extern u32 native_fn_0205d2cc();
extern u32 native_fn_0205d458();
extern u8 native_data_021043ac[];
u32 native_main_0205d53c(void) {
    s32 var_r5;
    u32 var_r6;
    u8 *var_r7;
    u8 temp_r0;

    var_r6 = 0;
    var_r7 = native_data_021043ac;
    var_r5 = 0;
    do {
        temp_r0 = *var_r7;
        if (temp_r0 == 3) {
            native_fn_0205cfd4(var_r7);
            native_fn_0205d068(var_r7);
            native_fn_0205d25c(var_r7);
            native_fn_0205d2cc(var_r7);
            native_fn_0205d458(var_r5);
            var_r6 += 1;
        } else if (temp_r0 == 4) {
            native_fn_0205cf5c(var_r7);
            *var_r7 = 0;
        }
        var_r5 += 1;
        var_r7 += 0x11C;
    } while (var_r5 < 0x20);
    return var_r6;
}
