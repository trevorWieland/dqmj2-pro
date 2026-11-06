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
    u8 field_0;
    u8 unknown_1[0x88];
    u8 field_89;
} Record_native_data_ov000_022381b4;
extern Record_native_data_ov000_022381b4 native_data_ov000_022381b4;
u32 native_ov000_022061a0(void) {
    if (((u32) (native_data_ov000_022381b4.field_0 << 0x1F) >> 0x1F) != 0) {
        return (u32) native_data_ov000_022381b4.field_89;
    }
    return 0U;
}
