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
extern u32 native_fn_02002480();
typedef struct {
    u8 unknown_0[0x4];
    u16 field_4;
} Record_native_data_ov006_0221c0ec;
extern Record_native_data_ov006_0221c0ec native_data_ov006_0221c0ec;
u32 native_ov006_021fb358(s32 arg0) {
    u32 var_r0;
    s32 var_r1;

    var_r0 = native_fn_02002480(native_data_ov006_0221c0ec.field_4, 0x1D);
    var_r1 = 0;
loop_1:
    if (var_r0 == arg0) {
        return (u32) var_r1;
    }
    var_r1 += 1;
    var_r0 += 1;
    if (var_r1 >= 4) {
        return -1U;
    }
    goto loop_1;
}
