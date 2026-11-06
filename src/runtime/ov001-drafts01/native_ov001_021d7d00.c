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
extern u32 native_fn_02008d78();
extern u8 native_data_ov001_0222fda0[];
u32 native_ov001_021d7d00(s32 arg0, s32 arg1) {
    s32 temp_r4;
    u32 var_r1;

    temp_r4 = (arg0 * 0x78) + (s32) native_data_ov001_0222fda0;
    var_r1 = 0;
    if ((M2C_FIELD(temp_r4, u8 *, 1) == 1) && (M2C_FIELD(temp_r4, s32 *, 0x1C) == 0)) {
        native_fn_02008d78(temp_r4 + 0x1C, 0, 0x5C);
        M2C_FIELD(temp_r4, s32 *, 0x1C) = arg1;
        var_r1 = 1;
    }
    return var_r1;
}
