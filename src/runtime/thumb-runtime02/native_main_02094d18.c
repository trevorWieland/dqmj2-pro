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
extern u32 native_fn_020946ec();
extern u32 native_fn_020948d0();
u32 native_main_02094d18(void *arg0) {
    s16 temp_r1;
    s32 temp_r1_2;
    u32 var_r0;

    var_r0 = native_fn_020946ec(0x10);
    temp_r1 = M2C_FIELD(arg0, s16 *, 0);
    if (temp_r1 == 5) {
        if (M2C_FIELD(arg0, s16 *, 2) != 0) {
            temp_r1_2 = M2C_FIELD(arg0, s32 *, 8);
            switch (temp_r1_2) {
            case 13:
                M2C_FIELD(var_r0, s8 *, 0xD14) = 1;
                return var_r0;
            case 15:
                M2C_FIELD(var_r0, s8 *, 0xD14) = 2;
                return var_r0;
            case 17:
                M2C_FIELD(var_r0, s8 *, 0xD14) = 3;
                return var_r0;
            default:
                M2C_FIELD(var_r0, s8 *, 0xD14) = 4;
                return var_r0;
            }
        } else {
            
            return var_r0;
        }
    } else {
        if (temp_r1 == 7) {
            var_r0 = native_fn_020948d0(M2C_FIELD(arg0, s32 *, 4));
        }
        return var_r0;
    }
}
