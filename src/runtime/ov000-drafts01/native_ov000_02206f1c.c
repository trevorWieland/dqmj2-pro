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
extern u32 native_fn_0203d234();
extern u32 native_fn_0203d24c();
extern u32 native_fn_ov000_02207018();
extern u32 native_fn_ov000_02208c90();
typedef struct {
    u8 unknown_0[0x2];
    s8 field_2;
} Record_native_data_ov000_022382c4;
extern Record_native_data_ov000_022382c4 native_data_ov000_022382c4;
u32 native_ov000_02206f1c(void) {
    u32 var_r4;

    var_r4 = 0;
    switch (native_data_ov000_022382c4.field_2) {
    default:
        break;
    case 0:
        if (native_fn_0203d24c() != 0) {
            native_data_ov000_022382c4.field_2 = 6;
        } else {
            native_data_ov000_022382c4.field_2 = 9;
        }
        break;
    case 6:
        if (native_fn_ov000_02207018(0) != 0) {
            native_data_ov000_022382c4.field_2 = 7;
        }
        break;
    case 7:
        if (native_fn_ov000_02207018(1) != 0) {
            native_data_ov000_022382c4.field_2 = 8;
        }
        break;
    case 8:
        if (native_fn_ov000_02207018(2) != 0) {
            native_fn_ov000_02208c90(7);
            native_data_ov000_022382c4.field_2 = 5;
        }
        break;
    case 9:
        if (native_fn_ov000_02207018(3) != 0) {
            native_data_ov000_022382c4.field_2 = 8;
        }
        break;
    case 5:
        native_fn_0203d234(0);
        var_r4 = 1;
        break;
    }
    return var_r4;
}
