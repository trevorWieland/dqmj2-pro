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
extern u32 native_fn_0203caa4();
extern u8 native_data_ov001_02242c4c[];
extern u8 native_data_ov001_02242c50[];
u32 native_ov001_02217fc8(void) {
    u32 var_r2;

    var_r2 = 0;
    if ((*native_data_ov001_02242c4c != 0) && (M2C_FIELD(native_data_ov001_02242c50, u8 *, 0x1E8) != 0) && (M2C_FIELD(native_data_ov001_02242c50, u8 *, 0x1E9) != 0)) {
        native_fn_0203caa4(native_data_ov001_02242c50, 0x41);
        var_r2 = 1;
    }
    return var_r2;
}
