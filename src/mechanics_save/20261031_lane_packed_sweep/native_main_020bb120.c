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
extern u32 native_fn_020685c8(s32 index);
extern u32 native_fn_02096df0(u32 record);
u32 native_main_020bb120(void) {
    u32 temp_r0;
    s32 var_r4;

    var_r4 = 0;
    do {
        temp_r0 = native_fn_02096df0(native_fn_020685c8(var_r4));
        var_r4 += 1;
    } while (var_r4 < 0x40);
    return temp_r0;
}
