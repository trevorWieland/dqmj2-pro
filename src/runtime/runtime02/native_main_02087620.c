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
u32 native_main_02087620(s32 arg0) {
    u32 var_r1;

    var_r1 = 1;
    switch (arg0) {
    case 11:
        var_r1 = 2;
        break;
    case 29:
        var_r1 = 2;
        break;
    case 17:
        var_r1 = 2;
        break;
    case 28:
        var_r1 = 2;
        break;
    }
    return var_r1;
}
