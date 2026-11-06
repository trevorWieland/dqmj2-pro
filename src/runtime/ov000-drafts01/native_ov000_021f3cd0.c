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
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_ov000_02236ed8;
extern Record_native_data_ov000_02236ed8 native_data_ov000_02236ed8;
u32 native_ov000_021f3cd0(u32 arg0) {
    u32 temp_r1;
    u32 var_r3;

    var_r3 = 0;
    if (arg0 < 8U) {
        temp_r1 = (arg0 * 0x27C) + native_data_ov000_02236ed8.field_4;
        if (M2C_FIELD(temp_r1, u8 *, 0x278) != 0) {
            var_r3 = temp_r1;
        }
    }
    return var_r3;
}
