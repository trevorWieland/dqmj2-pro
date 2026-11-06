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
extern u32 native_fn_02008e0c();
extern u32 native_fn_02048034();
extern u32 native_fn_0205dc70();
extern u32 native_fn_020bf014();
extern u32 native_fn_020bf218();
typedef struct {
    u8 unknown_0[0x4];
    u8 field_4;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e6d64(void) {
    u8 temp_r0;
    u32 temp_r4;

    temp_r0 = M2C_FIELD((void *) native_fn_020bf014(native_data_ov005_021ed438.field_4), u8 *, 0xAF);
    switch (temp_r0) {
    case 7:
        return native_fn_02048034(native_fn_0205dc70(0x13, 0, 0x1F), 0);
    case 8:
        return native_fn_02048034(native_fn_0205dc70(0x13, 0, 0x20), 0);
    case 9:
        return native_fn_02048034(native_fn_0205dc70(0x13, 0, 0x21), 0);
    default:
        temp_r4 = native_fn_020bf014(native_data_ov005_021ed438.field_4);
        native_fn_02008e0c(temp_r4, native_fn_020bf218(), 0x268);
        return native_fn_02048034(native_fn_020bf218() + 0xB0, 0);
    }
}
