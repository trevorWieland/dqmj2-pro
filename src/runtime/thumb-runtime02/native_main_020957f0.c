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
extern u32 native_fn_020946ec();
u32 native_main_020957f0(u32 arg0) {
    u32 temp_r0;
    u32 var_r4;

    var_r4 = arg0;
    temp_r0 = native_fn_020946ec(0x10);
    if (var_r4 > 0xDU) {
        var_r4 = 0xD;
    }
    M2C_FIELD(temp_r0, u16 *, 0xD16) = (u16) (M2C_FIELD(temp_r0, u16 *, 0xD16) | (1 << (var_r4 - 1)));
    return temp_r0;
}
