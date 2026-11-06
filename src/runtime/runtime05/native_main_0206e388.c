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
extern u32 native_fn_02061c1c();
extern u8 native_data_021c4f60[];
extern u8 native_data_021c4f98[];
u32 native_main_0206e388(s8 arg0, s8 arg1) {
    s8 var_r0;
    s8 var_r6;
    u8 *var_r7;
    u8 *var_r8;

    var_r7 = native_data_021c4f98;
    var_r6 = 0;
    var_r8 = native_data_021c4f98;
    do {
        if (var_r6 == 0) {
            var_r0 = arg0;
        } else {
            var_r0 = arg1;
        }
        if (var_r0 != -1) {
            M2C_FIELD(var_r8, s8 *, 0x10) = var_r0;
            native_fn_02061c1c(var_r0, (u8) M2C_FIELD(var_r7, s16 *, 0), (u8) M2C_FIELD(var_r7, s16 *, 2), 1, 2, 0, 1);
        }
        var_r6 += 1;
        var_r7 += 4;
        var_r8 += 1;
    } while ((s32) var_r6 < 2);
    M2C_FIELD(native_data_021c4f60, s32 *, 0x5C) = 1;
    return 0U;
}
