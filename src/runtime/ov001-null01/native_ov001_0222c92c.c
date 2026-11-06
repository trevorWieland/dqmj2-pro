#define NULL ((void *)0)
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
extern u32 native_fn_02008d78();
extern u32 native_fn_020649c0();
extern u32 native_fn_020649e8();
extern u32 native_fn_0207a9ec();
extern u32 native_fn_0207aad0();
extern u32 native_fn_ov001_0222c9ec();
extern u32 native_fn_ov001_0222cac8();
extern u32 native_fn_ov001_0222cd00();
extern u8 native_data_ov001_0224983c[];
extern u8 native_data_ov001_022498fc[];
u32 native_ov001_0222c92c(void) {
    u8 var_r8;
    u8 var_r8_2;

    native_fn_0207a9ec(1);
    native_fn_ov001_0222cac8();
    native_fn_ov001_0222cd00();
    var_r8 = 0;
    do {
        native_fn_02008d78(native_fn_020649c0(var_r8), 0, 0x210);
        native_fn_02008d78(native_fn_020649e8(var_r8), 0, 0x210);
        var_r8 += 1;
    } while ((u32) var_r8 < 3U);
    var_r8_2 = 0;
    do {
        native_fn_ov001_0222c9ec(native_fn_020649c0(var_r8_2), (var_r8_2 * 0x84) + (s32) native_data_ov001_022498fc, native_data_ov001_0224983c + (var_r8_2 << 6));
        native_fn_ov001_0222c9ec(native_fn_020649e8(var_r8_2), 0, NULL);
        var_r8_2 += 1;
    } while ((u32) var_r8_2 < 3U);
    return native_fn_0207aad0(1);
}
