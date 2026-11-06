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
extern u32 native_fn_02048a60();
extern u32 native_fn_0205f98c();
u32 native_main_0204b2d0(void *arg0, s32 arg1, void *arg2) {
    u32 temp_r0;
    u8 var_r4;
    s16 temp_r5;
    s16 var_r9;

    M2C_FIELD(arg0, s32 *, 0x2C) = arg1;
    temp_r0 = M2C_FIELD(arg0, u32 *, 0x1C);
    temp_r5 = M2C_FIELD(arg2, s16 *, 0);
    var_r9 = M2C_FIELD(arg2, s16 *, 2);
    if (temp_r0 == 0) {
        return temp_r0;
    }
    var_r4 = 0;
    do {
        native_fn_02048a60(native_fn_0205f98c(M2C_FIELD(arg0, u32 *, 0x1C), var_r4), temp_r5, var_r9);
        switch (arg1) {
        case 2:
            var_r9 += 0x68;
            break;
        case 0:
            var_r9 += 0x18;
            break;
        case 1:
            var_r9 += 0x40;
            break;
        }
        var_r4 += 1;
    } while ((u32) var_r4 < 2U);
    return native_fn_02048a60(native_fn_0205f98c(M2C_FIELD(arg0, u32 *, 0x1C), 2U), M2C_FIELD(arg2, s16 *, 0), M2C_FIELD(arg2, s16 *, 2));
}
