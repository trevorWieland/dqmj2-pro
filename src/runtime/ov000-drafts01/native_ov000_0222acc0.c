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
extern u32 native_fn_0205e7a8();
extern u32 native_fn_02063b28();
typedef struct {
    u8 unknown_0[0x20];
    s8 field_20;
    u8 unknown_21[0xdf];
    s8 field_100;
} Record_native_data_ov000_022475ec;
extern Record_native_data_ov000_022475ec native_data_ov000_022475ec;
u32 native_ov000_0222acc0(void) {
    s8 temp_r4;

    temp_r4 = native_data_ov000_022475ec.field_20;
    if (temp_r4 == 0) {
        native_data_ov000_022475ec.field_100 = 6;
        native_fn_02063b28(0x2F, 0);
        native_fn_0205e7a8(-1, 0x53);
    }
    return (u32) temp_r4;
}
