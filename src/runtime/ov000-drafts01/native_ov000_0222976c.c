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
extern u32 native_fn_0203d294();
extern u32 native_fn_02044d60();
extern u32 native_fn_02065d88();
extern u8 native_data_ov000_02247480[];
typedef struct {
    u8 unknown_0[0x1b];
    u8 field_1b;
} Record_native_data_ov000_022474c8;
extern Record_native_data_ov000_022474c8 native_data_ov000_022474c8;
u32 native_ov000_0222976c(void *arg0, void *arg1, u32 arg2) {
    u8 var_r4;

    M2C_FIELD(native_data_ov000_02247480, void **, 4) = arg0;
    M2C_FIELD(native_data_ov000_02247480, void **, 8) = arg1;
    var_r4 = 9;
    if (M2C_FIELD((void *) native_fn_02065d88(M2C_FIELD(arg0, u8 *, 0x31)), u8 *, 0x2A) == 1) {
        var_r4 = 0;
    }
    if (M2C_FIELD((void *) native_fn_02065d88(M2C_FIELD(M2C_FIELD(native_data_ov000_02247480, void **, 4), u8 *, 0x31)), u8 *, 0x2A) == 2) {
        var_r4 = 1;
    }
    if (M2C_FIELD((void *) native_fn_02065d88(M2C_FIELD(M2C_FIELD(native_data_ov000_02247480, void **, 8), u8 *, 0x31)), u8 *, 0x2A) == 1) {
        if (var_r4 == 1) {
            var_r4 = 9;
        } else {
            var_r4 = 0;
        }
    }
    if (M2C_FIELD((void *) native_fn_02065d88(M2C_FIELD(M2C_FIELD(native_data_ov000_02247480, void **, 8), u8 *, 0x31)), u8 *, 0x2A) == 2) {
        if (var_r4 == 0) {
            var_r4 = 9;
        } else {
            var_r4 = 1;
        }
    }
    if (var_r4 == 9) {
        if (native_fn_0203d294(0x11) == 0) {
            var_r4 = 2;
        } else {
            var_r4 = native_fn_0203d294(0x400) & 1;
        }
    }
    native_data_ov000_022474c8.field_1b = var_r4;
    if (native_fn_02044d60(arg2) != 0) {
        native_data_ov000_022474c8.field_1b = 2U;
    }
    return (u32) native_data_ov000_022474c8.field_1b;
}
