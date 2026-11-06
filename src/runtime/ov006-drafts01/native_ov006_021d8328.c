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
extern u8 native_data_ov006_0220ed54[];
u32 native_ov006_021d8328(s32 arg0) {
    u32 temp_r0;
    u32 temp_r0_2;
    s32 var_r1;
    u8 *var_r1_2;
    s32 var_r2_2;
    u8 *var_r2;

    if (arg0 == 1) {
        var_r2 = native_data_ov006_0220ed54;
        var_r1 = 0;
        do {
            var_r1 += 1;
            temp_r0_2 = M2C_FIELD(var_r2, u32 *, 0x7C) | 2;
            M2C_FIELD(var_r2, u32 *, 0x7C) = temp_r0_2;
            var_r2 += 0x90;
        } while (var_r1 < 0xA);
        return temp_r0_2;
    }
    var_r1_2 = native_data_ov006_0220ed54;
    var_r2_2 = 0;
    do {
        var_r2_2 += 1;
        temp_r0 = M2C_FIELD(var_r1_2, u32 *, 0x7C) & ~2;
        M2C_FIELD(var_r1_2, u32 *, 0x7C) = temp_r0;
        var_r1_2 += 0x90;
    } while (var_r2_2 < 0xA);
    return temp_r0;
}
