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
    u8 unknown_0[0x1c];
    s32 field_1c;
} Record_native_data_ov000_022463b0;
extern Record_native_data_ov000_022463b0 native_data_ov000_022463b0;
u32 native_ov000_0221f8a0(s32 arg0) {
    return M2C_FIELD(((arg0 * 0x84) + native_data_ov000_022463b0.field_1c), u32 *, 0x14);
}
