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
extern u32 native_fn_ov001_021e2cdc();
extern u32 native_fn_ov001_021e2e40();
extern u32 native_fn_ov001_021e2f20();
extern u32 native_fn_ov001_021e3000();
extern u32 native_fn_ov001_021e30d8();
typedef struct {
    u8 unknown_0[0x3];
    u8 field_3;
} Record_native_data_ov001_02238ad0;
extern Record_native_data_ov001_02238ad0 native_data_ov001_02238ad0;
u32 native_ov001_021e3168(void) {
    u32 var_r0;
    u32 var_r7;

    var_r0 = 1;
    var_r7 = 0;
    do {
        switch (native_data_ov001_02238ad0.field_3) {
        default:
            break;
        case 0:
            var_r0 = native_fn_ov001_021e2cdc();
            break;
        case 1:
            var_r0 = native_fn_ov001_021e2e40();
            break;
        case 2:
            var_r0 = native_fn_ov001_021e2f20();
            break;
        case 4:
            var_r0 = native_fn_ov001_021e3000();
            break;
        case 5:
            var_r0 = native_fn_ov001_021e30d8();
            break;
        case 3:
            var_r0 = 0;
            var_r7 = 1;
            break;
        }
    } while (var_r0 != 0);
    return var_r7;
}
