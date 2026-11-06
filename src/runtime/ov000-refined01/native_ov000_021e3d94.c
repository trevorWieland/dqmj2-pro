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
extern u8 native_data_ov000_0222ec58[];
extern u8 native_data_ov000_0222ec60[];
extern u8 native_data_ov000_0222ec68[];
extern u8 native_data_ov000_0222ec70[];
extern u8 native_data_ov000_0222ec74[];
extern u8 native_data_ov000_0222ec80[];
extern u8 native_data_ov000_0222ec88[];
extern u8 native_data_ov000_0222ec90[];
extern u8 native_data_ov000_0222ec98[];
extern u8 native_data_ov000_0222ec9c[];
extern u8 native_data_ov000_02234388[];
u32 native_ov000_021e3d94(void *arg0) {
    s32 temp_r0;
    u32 var_r0;
    u32 var_r4;
    s32 temp_r5;

    var_r4 = 0;
    temp_r0 = (s32) native_fn_ov000_021e3444();
    if (temp_r0 >= 0) {
        temp_r5 = (temp_r0 * 0x34) + (s32) native_data_ov000_02234388;
        var_r4 = 1;
        M2C_FIELD(temp_r5, s8 *, 0x1C) = 1;
        M2C_FIELD(temp_r5, s8 *, 0x2C) = 1;
        native_fn_ov000_021e3478(temp_r5, arg0, 5);
        if (native_fn_0201d914(arg0 + 5, native_data_ov000_0222ec58, 4) == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x21) = 3;
            M2C_FIELD(temp_r5, s8 *, 0x22) = 0;
        } else if (native_fn_0201d914(arg0 + 5, native_data_ov000_0222ec60, 4) == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x21) = 2;
            if (M2C_FIELD(arg0, s8 *, 9) == 0) {
                var_r0 = 0;
            } else {
                var_r0 = native_fn_0201f274(arg0 + 9);
            }
            M2C_FIELD(temp_r5, s8 *, 0x22) = (s8) var_r0;
        } else if (native_fn_0201d914(arg0 + 5, native_data_ov000_0222ec68, 4) == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x21) = 1;
            M2C_FIELD(temp_r5, s8 *, 0x22) = 0;
        } else if (native_fn_0201d914(arg0 + 5, native_data_ov000_0222ec70, 3) == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x21) = 0;
            M2C_FIELD(temp_r5, s8 *, 0x22) = 0;
        } else if (native_fn_0201d914(arg0 + 5, native_data_ov000_0222ec74, 8) == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x22) = 0;
        } else if (native_fn_0201d914(arg0 + 5, native_data_ov000_0222ec80, 6) == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x22) = 0;
        } else if (native_fn_0201d914(arg0 + 5, native_data_ov000_0222ec88, 5) == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x22) = 0;
        } else if (native_fn_0201d914(arg0 + 5, native_data_ov000_0222ec90, 5) == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x22) = 0;
        } else if (native_fn_0201d914(arg0 + 5, native_data_ov000_0222ec98, 3) == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x22) = 0;
        } else if (native_fn_0201d914(arg0 + 5, native_data_ov000_0222ec9c, 7) != 0) {
            var_r4 = 0;
            M2C_FIELD(temp_r5, s8 *, 0x1C) = 0;
        } else {
            M2C_FIELD(temp_r5, s8 *, 0x21) = 4;
            M2C_FIELD(temp_r5, s8 *, 0x22) = 0;
        }
    }
    return var_r4;
}
