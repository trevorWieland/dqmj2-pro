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
extern u32 native_fn_020273f0();
extern u32 native_fn_020414b0();
extern u32 native_fn_02041510();
extern u32 native_fn_02041764();
extern u32 native_fn_02041800();
extern u32 native_fn_02041898();
extern u32 native_fn_0206157c();
extern u32 native_fn_02062328();
extern u32 native_fn_ov000_021ea588();
extern u32 native_fn_ov000_021ea848();
extern u32 native_fn_ov000_021ea960();
extern u32 native_fn_ov000_021ea9fc();
extern u32 native_fn_ov000_021eaaac();
extern u32 native_fn_ov000_021eb030();
extern u8 native_data_ov000_02236950[];
u32 native_ov000_021ea25c(void) {
    u32 var_r4;
    s32 var_r5;

    M2C_FIELD(native_data_ov000_02236950, s8 *, 2) = 1;
    var_r4 = 6;
    var_r5 = 0;
    switch (M2C_FIELD(native_data_ov000_02236950, s8 *, 5)) {
    default:
        break;
    case 0:
        M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 1;
        break;
    case 1:
        M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 2;
        native_fn_02041898(0);
        break;
    case 2:
        native_fn_ov000_021ea588();
        M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 3;
        var_r5 = 1;
        break;
    case 3:
        native_fn_0206157c();
        M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 4;
        var_r5 = 1;
        break;
    case 4:
        native_fn_0206157c();
        native_fn_ov000_021ea960();
        native_fn_ov000_021ea9fc();
        if (M2C_FIELD(native_data_ov000_02236950, u8 *, 6) != 0) {
            native_fn_02041510(1, 2, 0x1E);
            M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 7;
        }
        if (M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), s16 *, 0x1F2) != M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), s16 *, 0x1F0)) {
            M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 7;
        }
        break;
    case 5:
        native_fn_ov000_021ea848();
        M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 6;
        break;
    case 6:
        if (native_fn_ov000_021eaaac() != 0) {
            if (M2C_FIELD(native_data_ov000_02236950, u8 *, 6) == 0) {
                M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 4;
            } else {
                native_fn_020414b0(0x3F);
                native_fn_02041510(1, 2, 0x1E);
                M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 7;
            }
        }
        break;
    case 7:
        native_fn_ov000_021ea848();
        if (M2C_FIELD(native_data_ov000_02236950, u8 *, 6) != 0) {
            M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 8;
        } else {
            M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 2;
            M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), s16 *, 0x1F0) = (s16) M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), s16 *, 0x1F2);
            M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), u8 *, 0x1F4) = (u8) M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), u8 *, 0x1F5);
        }
        break;
    case 8:
        if ((native_fn_02041800() != 1) && (native_fn_020273f0() == 0)) {
            native_fn_02062328();
            native_fn_ov000_021eb030();
            native_fn_ov000_021ea960();
            M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 9;
        }
        break;
    case 9:
        var_r4 = 1;
        break;
    }
    if (var_r5 != 0) {
        return native_ov000_021ea25c();
    }
    native_fn_02041764();
    return var_r4;
}
