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
extern u32 native_fn_0201d914();
extern u32 native_fn_0201f274();
extern u32 native_fn_ov000_021e3444();
extern u32 native_fn_ov000_021e3478();
extern u8 native_data_ov000_0222ec50[];
extern u8 native_data_ov000_02234388[];
u32 native_ov000_021e3d1c(s32 arg0) {
    s32 temp_r0;
    u32 var_r4;
    s32 temp_r5;

    var_r4 = 0;
    temp_r0 = (s32) native_fn_ov000_021e3444();
    if (temp_r0 >= 0) {
        temp_r5 = (temp_r0 * 0x34) + (s32) native_data_ov000_02234388;
        native_fn_ov000_021e3478(temp_r5, arg0, 7);
        if (native_fn_0201d914(arg0 + 2, native_data_ov000_0222ec50, 7) == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x1E) = (s8) native_fn_0201f274(arg0 + 9);
            M2C_FIELD(temp_r5, s8 *, 0x20) = 2;
        }
        var_r4 = 1;
        M2C_FIELD(temp_r5, s8 *, 0x1C) = 1;
    }
    return var_r4;
}
