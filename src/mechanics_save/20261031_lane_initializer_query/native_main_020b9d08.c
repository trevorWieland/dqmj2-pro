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
typedef struct {
    u32 field_0;
    s32 field_4;
} Record_native_data_021d3038;
extern Record_native_data_021d3038 native_data_021d3038;
u32 native_main_020b9d08(u32 arg0, s32 arg1) {
    s32 var_r1;

    var_r1 = arg1;
    if (var_r1 > -10000) {
        var_r1 -= 0x2710;
    }
    if (native_data_021d3038.field_0 != 9) {
        native_data_021d3038.field_0 = arg0;
        native_data_021d3038.field_4 = var_r1;
    }
    return arg0;
}
