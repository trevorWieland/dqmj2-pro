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
extern u32 native_fn_ov001_021e80c0();
extern u32 native_fn_ov001_021fbd6c();
extern u32 native_fn_ov001_021fbe70();
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
    u8 unknown_9[0x14];
    s8 field_1d;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
u32 native_ov001_021df9e4(void) {
    if (native_fn_ov001_021fbd6c() != 0) {
        if (native_fn_ov001_021fbe70() != 0) {
            native_data_ov001_022388ec.field_8 = 0x15;
        } else {
            native_fn_ov001_021e80c0();
            native_data_ov001_022388ec.field_1d = 1;
            native_data_ov001_022388ec.field_8 = 3;
        }
    }
    return 0U;
}
