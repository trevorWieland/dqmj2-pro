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

u32 native_arm7_main_027e1a40(s32 arg0) {
    s32 var_r0;

    var_r0 = arg0 >> 2;
    if (!(arg0 & 2)) {
        var_r0 += 0x19;
    }
    return (u32) (u8) var_r0;
}
