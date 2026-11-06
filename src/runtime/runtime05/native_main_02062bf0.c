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
extern u32 native_fn_02062a50();
u32 native_main_02062bf0(s32 arg0, s32 arg1) {
    s32 var_r4;
    u32 temp_r0;
    u32 var_r5;

    var_r5 = 0;
    var_r4 = 0;
    do {
        temp_r0 = native_fn_02062a50(var_r4);
        if ((temp_r0 != 0) && (M2C_FIELD(temp_r0, s16 *, 0x18) == arg0)) {
            if ((arg1 != 4) && (M2C_FIELD(temp_r0, u8 *, 0x1A) != arg1)) {

            } else {
                var_r5 += 1;
            }
        }
        var_r4 += 1;
    } while (var_r4 < 3);
    return var_r5;
}
