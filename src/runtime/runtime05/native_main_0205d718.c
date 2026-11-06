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
extern u8 native_data_021043ac[];
u32 native_main_0205d718(u32 arg0) {
    s32 temp_r1;
    u32 var_r3;

    var_r3 = 0;
    if (arg0 < 0x20U) {
        temp_r1 = arg0 * 0x11C;
        if (*(native_data_021043ac + temp_r1) == 3) {
            *(native_data_021043ac + temp_r1) = 4;
            var_r3 = 1;
        }
    }
    return var_r3;
}
