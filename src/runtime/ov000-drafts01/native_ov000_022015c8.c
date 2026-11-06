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
extern u8 native_data_ov000_02237d94[];
u32 native_ov000_022015c8(void) {
    s32 var_r2;
    u8 *var_r3;
    u8 temp_r1;
    u8 var_r0;

    var_r0 = 0;
    var_r3 = native_data_ov000_02237d94;
    var_r2 = 0;
    do {
        temp_r1 = M2C_FIELD(var_r3, u8 *, 0x1EC);
        var_r2 += 1;
        var_r3 += 1;
        if (temp_r1 != 0x7F) {
            var_r0 += 1;
        }
    } while (var_r2 < 0xC);
    return (u32) var_r0;
}
