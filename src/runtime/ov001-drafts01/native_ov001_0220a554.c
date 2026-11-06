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
extern u32 native_fn_0206de1c();
extern u32 native_fn_0207aad0();
extern u32 native_fn_0207e948();
extern u32 native_fn_ov001_0220a9ec();
extern u32 native_fn_ov001_0220b2f0();
typedef struct {
    u8 unknown_0[0x6];
    u8 field_6;
    u8 unknown_7[0xd];
    s32 field_14;
} Record_native_data_ov001_0223def8;
extern Record_native_data_ov001_0223def8 native_data_ov001_0223def8;
u32 native_ov001_0220a554(void) {
    if (native_data_ov001_0223def8.field_14 == 0) {
        native_fn_0207e948();
    }
    if (native_data_ov001_0223def8.field_6 != 0) {
        native_fn_ov001_0220b2f0();
        native_fn_ov001_0220a9ec();
    }
    native_fn_0207aad0(2);
    return native_fn_0206de1c(0, 0);
}
