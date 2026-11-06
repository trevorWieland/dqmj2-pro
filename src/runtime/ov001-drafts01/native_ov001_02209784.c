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
extern u32 native_fn_ov001_0220349c();
extern u32 native_fn_ov001_0220984c();
extern u32 native_fn_ov001_02209cc0();
extern u32 native_fn_ov001_0220a104();
extern u32 native_fn_ov001_0220a1c8();
extern u32 native_fn_ov001_0220a41c();
extern u32 native_fn_ov001_0220a450();
extern u32 native_fn_ov001_0220a46c();
extern u32 native_fn_ov001_0220a554();
typedef struct {
    u8 unknown_0[0x20];
    u32 field_20;
} Record_native_data_ov001_0223def8;
extern Record_native_data_ov001_0223def8 native_data_ov001_0223def8;
u32 native_ov001_02209784(void) {
    u32 var_r4;

    var_r4 = 0;
    switch (native_data_ov001_0223def8.field_20) {
    default:
        break;
    case 0:
        native_data_ov001_0223def8.field_20 = native_fn_ov001_0220984c();
        break;
    case 1:
        native_data_ov001_0223def8.field_20 = native_fn_ov001_02209cc0();
        break;
    case 2:
        native_data_ov001_0223def8.field_20 = native_fn_ov001_0220a104();
        break;
    case 3:
        native_data_ov001_0223def8.field_20 = native_fn_ov001_0220a1c8();
        break;
    case 4:
        native_data_ov001_0223def8.field_20 = native_fn_ov001_0220a41c();
        break;
    case 5:
        native_data_ov001_0223def8.field_20 = native_fn_ov001_0220a450();
        break;
    case 6:
        native_data_ov001_0223def8.field_20 = native_fn_ov001_0220a46c();
        break;
    case 7:
        native_fn_ov001_0220349c(native_fn_ov001_0220a554);
        var_r4 = 1;
        break;
    }
    return var_r4;
}
