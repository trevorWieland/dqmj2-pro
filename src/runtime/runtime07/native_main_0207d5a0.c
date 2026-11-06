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
extern u32 native_fn_0207d2c8();
u32 native_main_0207d5a0(s32 arg0, u32 arg1, s32 arg2) {
    u32 temp_r0;
    u32 var_r5;
    u8 temp_r0_2;
    u8 temp_r1;

    var_r5 = arg1;
    temp_r0 = native_fn_0207d2c8();
    if (arg0 == 0) {
        return var_r5;
    }
    temp_r1 = M2C_FIELD(temp_r0, u8 *, 3);
    if ((temp_r1 == 1) && (arg2 == 1)) {
        temp_r0_2 = M2C_FIELD(temp_r0, u8 *, 4);
        switch (temp_r0_2) {
        default:
            break;
        case 1:
            var_r5 = 6;
            break;
        case 2:
            var_r5 = 8;
            break;
        case 3:
            var_r5 = 0xA;
            break;
        case 4:
            var_r5 = 0xC;
            break;
        }
    }
    if ((temp_r1 == 9) && (arg2 == 6)) {
        var_r5 *= 2;
    }
    return var_r5;
}
