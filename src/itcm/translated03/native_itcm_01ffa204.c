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
extern u8 native_data_021cecf4[];
u32 native_itcm_01ffa204(void) {
    s32 var_r1;
    u8 *var_r2;

    var_r1 = 0;
    var_r2 = native_data_021cecf4;
    do {
        var_r1 += 1;
        M2C_FIELD(var_r2, s8 *, 0x16C) = 0;
        var_r2 += 0x170;
    } while (var_r1 < 8);
    return 0U;
}
