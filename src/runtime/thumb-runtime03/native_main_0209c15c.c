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
extern u32 native_fn_0209becc();
u32 native_main_0209c15c(u32 arg0, void *arg1) {
    s32 temp_r1;
    u32 var_r0;

    temp_r1 = M2C_FIELD(arg1, s32 *, 4);
    var_r0 = 0x603;
    if (temp_r1 != 0x603) {
        var_r0 = 0x901;
        if (temp_r1 != 0x901) {
            var_r0 = 0xB01;
            if (temp_r1 != 0xB01) {
                var_r0 = native_fn_0209becc(3);
            }
        }
    }
    return var_r0;
}
