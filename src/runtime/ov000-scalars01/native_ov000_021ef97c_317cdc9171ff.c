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
extern u32 native_fn_ov000_021ef688();
extern u32 native_fn_ov000_021ef77c();
extern u8 native_data_ov000_0222ee80[];
typedef struct {
    u8 field_0;
    u8 unknown_1[0x3];
    s16 field_4;
} Record_native_data_ov000_02236c1c;
extern Record_native_data_ov000_02236c1c native_data_ov000_02236c1c;
u32 native_ov000_021ef97c(s32 arg0) {
    u32 temp_r0;
    u8 var_r1;

    if (arg0 != 0) {
        var_r1 = 0xD;
    } else {
        var_r1 = 0x1C;
    }
    native_data_ov000_02236c1c.field_0 = var_r1;
    temp_r0 = native_fn_ov000_021ef688(0x10, 5, 2, 2, 0x15, (s32) var_r1, 2, 0, 1);
    if (temp_r0 == 0) {
        return temp_r0;
    }
    native_data_ov000_02236c1c.field_4 = 0x10;
    native_fn_ov000_021ef77c(0x10, 9, 2, 6, 0x10, 0);
    *(u32 *)native_data_ov000_0222ee80 = 1;
    return (u32) native_data_ov000_0222ee80;
}
