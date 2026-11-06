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
extern u8 native_data_020ec360[];
u32 native_main_02018930(void) {
    s32 var_ip;
    s32 var_r1;
    s32 var_r2;
    s32 var_r3;

    if (M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), u16 *, 0x12) != 0) {
        var_r2 = 2;
    } else {
        var_r2 = 0;
    }
    if (M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), u16 *, 0xE) != 0) {
        var_r3 = 1;
    } else {
        var_r3 = 0;
    }
    if (M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), u16 *, 0x14) != 0) {
        var_ip = 4;
    } else {
        var_ip = 0;
    }
    if (M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), u16 *, 0x16) != 0) {
        var_r1 = 8;
    } else {
        var_r1 = 0;
    }
    return (u32) (u8) (var_r1 | (var_ip | (var_r3 | var_r2)));
}
