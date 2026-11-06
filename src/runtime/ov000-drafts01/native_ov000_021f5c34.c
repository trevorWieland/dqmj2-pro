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
extern u32 native_fn_02061944();
extern u32 native_fn_ov000_021f65e4();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
    u8 unknown_8[0xc];
    s32 field_14;
    s32 field_18;
    u8 unknown_1c[0x8];
    s32 field_24;
} Record_native_data_ov000_02236ee4;
extern Record_native_data_ov000_02236ee4 native_data_ov000_02236ee4;
u32 native_ov000_021f5c34(void) {
    u32 temp_r4;
    u32 var_r5;

    temp_r4 = native_fn_02061944();
    var_r5 = 0;
    native_fn_ov000_021f65e4(9, native_data_ov000_02236ee4.field_14, 3);
    native_fn_ov000_021f65e4(0xB, native_data_ov000_02236ee4.field_24, 3);
    native_fn_ov000_021f65e4(0xD, native_data_ov000_02236ee4.field_18, 3);
    native_fn_ov000_021f65e4(0xF, native_data_ov000_02236ee4.field_4, 3);
    if (M2C_FIELD(temp_r4, s8 *, 0x26C) != 0x2A) {
        var_r5 = 1;
    }
    return var_r5;
}
