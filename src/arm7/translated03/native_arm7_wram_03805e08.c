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
extern u32 native_arm7_data_03807564;
u32 native_arm7_wram_03805e08(u32 arg0, u32 arg1) {
    s32 var_r3;
    u32 var_r0;

    var_r0 = arg0;
    var_r3 = 0;
    do {
        if (var_r0 & 1) {
            (&native_arm7_data_03807564)[var_r3] = arg1;
        }
        var_r3 += 1;
        var_r0 = var_r0 >> 1;
    } while (var_r3 < 0x19);
    return var_r0;
}
