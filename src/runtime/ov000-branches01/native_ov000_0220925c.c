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
    s16 field_0;
    s16 field_2;
    u16 field_4;
    u16 field_6;
    s8 field_8;
} Record_native_data_ov000_02238520;
extern Record_native_data_ov000_02238520 native_data_ov000_02238520;
u32 native_ov000_0220925c(s16 arg0, s32 arg1) {
    s32 var_r1;
    u32 temp_r3;

    var_r1 = arg1;
    temp_r3 = native_data_ov000_02238520.field_0 | (native_data_ov000_02238520.field_2 << 0x10);
    if (var_r1 < 0) {
        if (native_data_ov000_02238520.field_8 == 0) {
            var_r1 = (s32) (u8) (native_data_ov000_02238520.field_4 + 0xC0);
        } else {
            var_r1 = (s32) (u8) (native_data_ov000_02238520.field_6 + 0xC0);
        }
    }
    native_data_ov000_02238520.field_0 = arg0;
    native_data_ov000_02238520.field_2 = (s16) var_r1;
    return temp_r3;
}
