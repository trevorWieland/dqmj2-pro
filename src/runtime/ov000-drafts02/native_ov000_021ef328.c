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
extern u32 native_fn_0205f98c();
extern u8 native_data_ov000_0222ee64[];
extern u8 native_data_ov000_02236bd0[];
void native_ov000_021ef328(s32 arg0, s32 arg1) {
    u32 temp_r0;
    s32 var_r1;
    u8 var_r4;

    var_r4 = 0;
    do {
        temp_r0 = native_fn_0205f98c(M2C_FIELD(M2C_FIELD(native_data_ov000_02236bd0, void **, 0x10), s32 *, 0x1C), var_r4);
        if (var_r4 == 0) {
            var_r1 = arg0;
        } else {
            var_r1 = arg1;
        }
        if ((var_r1 != 0) && (*native_data_ov000_0222ee64 != 0)) {
            M2C_FIELD(temp_r0, s32 *, 0x7C) = (s32) (M2C_FIELD(temp_r0, s32 *, 0x7C) | 2);
        } else {
            M2C_FIELD(temp_r0, s32 *, 0x7C) = (s32) (M2C_FIELD(temp_r0, s32 *, 0x7C) & ~2);
        }
        var_r4 += 1;
    } while ((u32) var_r4 < 2U);
}
