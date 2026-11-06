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
extern u32 native_fn_ov001_021d7584();
extern u8 native_data_ov001_0222fd50[];
u32 native_ov001_021d72e0(void) {
    s32 var_r4;
    u8 *var_r5;

    var_r5 = native_data_ov001_0222fd50;
    var_r4 = 0;
    do {
        if (M2C_FIELD(var_r5, u8 *, 0x51) == 2) {
            native_fn_ov001_021d7584(var_r4);
        }
        var_r4 += 1;
        var_r5 += 0x78;
    } while (var_r4 < 0x31);
    return native_fn_02008d78(native_data_ov001_0222fd50, 0, 0x176C);
}
