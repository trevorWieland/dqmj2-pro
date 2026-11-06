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
extern u32 native_fn_020a8ef8();
u32 native_main_020b8068(void *arg0) {
    s32 var_r4;
    u32 temp_r0;
    void *var_r5;

    var_r5 = arg0;
    var_r4 = 0;
    temp_r0 = native_fn_020a8ef8();
    do {
        if ((M2C_FIELD(var_r5, s32 *, 0x118) != 0) && ((u32) (temp_r0 - M2C_FIELD(var_r5, s32 *, 0x120)) > 0xFA0U)) {
            M2C_FIELD(var_r5, s32 *, 0x118) = 0;
        }
        var_r4 += 1;
        var_r5 += 0x10;
    } while (var_r4 < 0xC8);
    return temp_r0;
}
