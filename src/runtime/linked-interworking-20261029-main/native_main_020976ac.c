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
extern u32 native_fn_02008d78();
extern u32 native_fn_02008e0c();
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
} Record_native_data_021d18f0;
extern Record_native_data_021d18f0 native_data_021d18f0;
u32 native_main_020976ac(s32 *arg0) {
    s32 var_r0;
    s32 temp_r1;
    s32 temp_r1_2;

    if (native_data_021d18f0.field_8 == 0) {
        native_fn_02008d78(arg0, 0, 0x1C4);
    }
    native_fn_02008e0c(native_data_021d18f0.field_8 + 0x1008, arg0, 0x1C4);
    temp_r1 = *arg0;
    if ((temp_r1 < 0x4E20) || (temp_r1 >= 0x7530)) {
        *arg0 = 0x5206;
    }
    temp_r1_2 = *arg0;
    var_r0 = 0x4E84;
    if (temp_r1_2 >= 0x4E84) {
        var_r0 = 0 - temp_r1_2;
        *arg0 = var_r0;
    }
    return (u32) var_r0;
}
