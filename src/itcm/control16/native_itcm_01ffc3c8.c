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
extern u32 native_data_021d4100;
extern volatile s8 native_data_021d41f4[8];
extern volatile s8 native_data_021d41fc[64];
u32 native_itcm_01ffc3c8(void) {
    volatile s8 *var_r0;
    s32 var_r1;
    s32 var_r2;

    var_r2 = (s32)native_data_021d41f4;
    var_r1 = 0;
    do {
        *(volatile s8 *)var_r2 = -1;
        var_r2 += 1;
        var_r1 += 1;
    } while (var_r1 < 8);
    var_r2 = 0;
    var_r0 = native_data_021d41fc;
    do {
        *var_r0++ = 0;
        var_r2 += 1;
    } while (var_r2 < 0x40);
    M2C_FIELD(&native_data_021d4100, s8 *, 2) = 0;
    M2C_FIELD(&native_data_021d4100, s8 *, 0) = 0;
    M2C_FIELD(&native_data_021d4100, s8 *, 1) = 0;
    return (u32) &native_data_021d4100;
}
