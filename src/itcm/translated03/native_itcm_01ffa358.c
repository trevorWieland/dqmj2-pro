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
extern u32 native_fn_020846bc();
u32 native_itcm_01ffa358(void) {
    s32 var_r2;
    u16 var_r4;
    u32 var_r0;

    var_r4 = 0;
    var_r0 = native_fn_020846bc();
    var_r2 = 0;
    do {
        var_r2 += 1;
        if (var_r0 != 0) {
            var_r4 += 1;
        }
        var_r0 = (u32) (var_r0 << 0xF) >> 0x10;
    } while (var_r2 < 8);
    return (u32) var_r4;
}
