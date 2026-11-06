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
extern u32 native_fn_020414c8();
extern u32 native_fn_02048f7c();
extern u32 native_fn_02049b84();
extern u32 native_fn_0204b61c();
typedef struct {
    u8 unknown_0[0x2c];
    s32 field_2c;
} Record_native_data_ov000_0224532c;
extern Record_native_data_ov000_0224532c native_data_ov000_0224532c;
extern u8 native_data_ov000_0224535c[];
u32 native_ov000_02217c9c(s32 arg0) {
    u32 temp_r0;

    native_fn_02049b84();
    if (arg0 != 0) {
        native_fn_020414c8(0x3F);
    }
    if (native_data_ov000_0224532c.field_2c != 0) {
        native_fn_0204b61c(native_data_ov000_0224532c.field_2c, 1);
    }
    temp_r0 = native_fn_02048f7c(1);
    *(u32 *)(native_data_ov000_0224535c + (temp_r0 * 4)) = 0x20;
    return temp_r0;
}
