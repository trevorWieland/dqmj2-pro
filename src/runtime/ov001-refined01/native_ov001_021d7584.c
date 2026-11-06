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
extern u32 native_fn_0202a1e0();
extern u32 native_fn_0202a260();
extern u32 native_fn_0202a280();
extern u32 native_fn_02044698();
extern u8 native_data_ov001_0222fda0[];
u32 native_ov001_021d7584(s32 arg0) {
    u32 var_r4;
    s32 temp_r5;

    temp_r5 = (arg0 * 0x78) + (s32) native_data_ov001_0222fda0;
    var_r4 = 0;
    if (M2C_FIELD(temp_r5, s32 *, 0x4C) != 0) {
        native_fn_0202a260();
        native_fn_0202a1e0(1);
        var_r4 = native_fn_02044698(temp_r5 + 0x1C);
        native_fn_0202a280();
        M2C_FIELD(temp_r5, s32 *, 0x4C) = 0;
    }
    return var_r4;
}
