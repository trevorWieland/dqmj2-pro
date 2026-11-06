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
    u8 unknown_0[0x2f];
    u8 field_2f;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
u32 native_ov001_021e2a64(s32 arg0) {
    s32 temp_r2;
    u32 var_r3;

    var_r3 = 0;
loop_1:
    temp_r2 = var_r3 - 1;
    if (arg0 == (1 << temp_r2)) {
        return (u32) ((s32) (native_data_ov001_022388ec.field_2f & arg0) >> temp_r2);
    }
    var_r3 += 1;
    if (var_r3 >= 8U) {
        return 0U;
    }
    goto loop_1;
}
