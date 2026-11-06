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
extern u32 native_fn_ov001_021e1328();
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
    s8 field_2;
    s8 field_3;
    u8 unknown_4[0x8];
    u32 field_c;
} Record_native_data_ov001_0223e0d8;
extern Record_native_data_ov001_0223e0d8 native_data_ov001_0223e0d8;
u32 native_ov001_0220d6a4(void) {
    s8 temp_r0;
    s8 var_r2;
    u32 temp_r0_2;

    native_data_ov001_0223e0d8.field_2 = 0;
    temp_r0_2 = native_fn_ov001_021e1328();
    native_data_ov001_0223e0d8.field_c = temp_r0_2;
    if (M2C_FIELD(temp_r0_2, s8 *, 0x24A) != 0) {
        var_r2 = 1;
    } else {
        var_r2 = 0;
    }
    native_data_ov001_0223e0d8.field_3 = var_r2;
    temp_r0 = M2C_FIELD(temp_r0_2, s8 *, 0x232);
    native_data_ov001_0223e0d8.field_1 = temp_r0;
    return (u32) temp_r0;
}
