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
extern u8 native_data_021c72a0[];
u32 native_main_02083eb4(void) {
    s32 temp_r1;
    s32 var_r0;

    var_r0 = ((M2C_FIELD(native_data_021c72a0, u16 *, 6) * (M2C_FIELD(native_data_021c72a0, u8 *, 3) + 1)) + 0x27) & ~0x1F;
    temp_r1 = (M2C_FIELD(native_data_021c72a0, u16 *, 6) + 0x21) & ~0x1F;
    if (var_r0 < temp_r1) {
        var_r0 = temp_r1;
    }
    return (u32) var_r0;
}
