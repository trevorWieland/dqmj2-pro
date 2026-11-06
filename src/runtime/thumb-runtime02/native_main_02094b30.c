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
extern u32 native_fn_02094bcc();
extern u32 native_fn_02094c14();
u32 native_main_02094b30(s32 arg0, void *arg1, u32 arg2, void *arg3) {
    u32 sp4;
    s32 sp0;
    s32 var_r0;
    u8 temp_r1;
    u8 temp_r3;
    void *var_r2;

    sp0 = arg0;
    sp4 = -1U;
    temp_r3 = M2C_FIELD(arg3, u8 *, 0xD12);
    var_r0 = 0;
    if ((s32) temp_r3 > 0) {
        var_r2 = arg3 + 0x474;
loop_2:
        if ((M2C_FIELD(arg1, u8 *, 4) == M2C_FIELD(var_r2, u8 *, 0)) && (M2C_FIELD(arg1, u8 *, 5) == M2C_FIELD(var_r2, u8 *, 1)) && (M2C_FIELD(arg1, u8 *, 6) == M2C_FIELD(var_r2, u8 *, 2)) && (M2C_FIELD(arg1, u8 *, 7) == M2C_FIELD(var_r2, u8 *, 3)) && (M2C_FIELD(arg1, u8 *, 8) == M2C_FIELD(var_r2, u8 *, 4)) && (M2C_FIELD(arg1, u8 *, 9) == M2C_FIELD(var_r2, u8 *, 5))) {
            sp4 = var_r0;
        } else {
            var_r0 += 1;
            var_r2 += 0xC0;
            if (var_r0 < (s32) temp_r3) {
                goto loop_2;
            }
        }
    }
    if (sp4 == -1) {
        native_fn_02094bcc((u8) sp0, arg1, arg2, arg3);
        temp_r1 = M2C_FIELD(arg3, u8 *, 0xD12);
        if ((u32) temp_r1 < 0xAU) {
            M2C_FIELD(arg3, u8 *, 0xD12) = (u8) (temp_r1 + 1);
        }
        sp4 = 0xA;
    } else {
        native_fn_02094c14((u32) sp4, arg1, arg2, arg3);
    }
    return sp4;
}
