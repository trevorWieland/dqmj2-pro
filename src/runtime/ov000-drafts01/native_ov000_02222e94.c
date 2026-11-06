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
extern u32 native_fn_0201d444();
extern u32 native_fn_020414b0();
extern u32 native_fn_02041510();
extern u32 native_fn_020653d0();
extern u32 native_fn_ov000_02223328();
extern u32 native_fn_ov000_02223390();
extern u8 native_data_ov000_0222fcf0[];
extern u8 native_data_ov000_0222fcfc[];
extern u8 native_data_ov000_0222fd0c[];
extern u8 native_data_ov000_02246574[];
u32 native_ov000_02222e94(void) {
    u8 sp0[32];
    u32 temp_r0;

    temp_r0 = native_fn_020653d0();
    switch (temp_r0) {
    case 0:
    case 3:
        native_fn_0201d444(&sp0, native_data_ov000_0222fcf0);
        break;
    case 5:
        native_fn_0201d444(&sp0, native_data_ov000_0222fcfc);
        break;
    default:
        native_fn_0201d444(&sp0, native_data_ov000_0222fd0c);
        break;
    }
    native_fn_ov000_02223390(&sp0);
    native_fn_020414b0(0x3F);
    native_fn_02041510(0, 2, 0xA);
    native_fn_ov000_02223328();
    *native_data_ov000_02246574 = 6;
    return (u32) native_data_ov000_02246574;
}
