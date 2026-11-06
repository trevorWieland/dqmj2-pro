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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_ov000_02213fa4();
extern u8 native_data_ov000_02243e3c[];
u32 native_ov000_02214008(void) {
    s32 var_r4;
    u32 var_r5;
    u8 *var_r6;
    u8 temp_r0;

    var_r5 = 0;
    var_r6 = native_data_ov000_02243e3c;
    var_r4 = 0;
    do {
        if ((M2C_FIELD(var_r6, u8 *, 0x105) != 0) && ((temp_r0 = M2C_FIELD(var_r6, u8 *, 0x107), (temp_r0 == 0)) || ((u32) (temp_r0 - 5) <= 1U)) && (native_fn_ov000_02213fa4(M2C_FIELD(var_r6, u8 *, 0x106)) != 0)) {
            var_r5 += 1;
        }
        var_r4 += 1;
        var_r6 += 0x10C;
    } while (var_r4 < 0x10);
    return var_r5;
}
