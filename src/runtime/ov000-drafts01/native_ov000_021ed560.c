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
extern u32 native_fn_0205e7a8();
extern u32 native_fn_ov000_021ef154();
extern u32 native_fn_ov000_021ef17c();
extern u32 native_fn_ov000_021efe60();
extern u32 native_fn_ov000_021effec();
extern u8 native_data_ov000_02236bc4[];
u32 native_ov000_021ed560(u8 *arg0) {
    s8 var_r4;

    var_r4 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x20);
    switch (var_r4) {
    default:
        break;
    case 0:
        M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x100) = 6;
        native_fn_0205e7a8(-1, 0x53);
        break;
    case 1:
    case 2:
        if (M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), u8 *, 0x101) == 1) {
            M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), u8 *, 0x101) = 0U;
            native_fn_ov000_021effec();
            native_fn_ov000_021efe60(1);
            native_fn_ov000_021ef17c(1);
            native_fn_ov000_021ef154(1);
            *arg0 |= 7;
        } else {
            if (var_r4 == 1) {
                M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x519) = 1;
            }
            var_r4 = 0;
        }
        native_fn_0205e7a8(-1, 0x53);
        break;
    case 3:
        var_r4 = 1;
        native_fn_0205e7a8(-1, 0x53);
        break;
    case 4:
        var_r4 = 3;
        native_fn_0205e7a8(-1, 0x53);
        break;
    }
    return (u32) var_r4;
}
