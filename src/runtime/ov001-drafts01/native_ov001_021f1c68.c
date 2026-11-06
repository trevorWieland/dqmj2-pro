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
extern u32 native_fn_ov001_021e1328();
extern u32 native_fn_ov001_021e1338();
extern u32 native_fn_ov001_021e1348();
extern u8 native_data_ov001_0223989c[];
extern u8 native_data_ov001_0223995c[];
extern u8 native_data_ov001_022399b8[];
u32 native_ov001_021f1c68(s8 arg0) {
    if (arg0 == 3) {
        M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x84) = (u32) M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x60);
        M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x80) = native_fn_ov001_021e1328();
    } else if (arg0 == 2) {
        M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x84) = native_fn_ov001_021e1328();
        M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x80) = (u32) M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x64);
    } else {
        M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x84) = native_fn_ov001_021e1328();
        M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x80) = native_fn_ov001_021e1338();
    }
    M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x78) = (u32) M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x84);
    M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x11) = (s8) native_fn_ov001_021e1348();
    M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x35) = arg0;
    M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x10) = 0;
    M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x13) = 0;
    M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x30) = 0;
    native_fn_02008d78(native_data_ov001_0223995c, 0, 3);
    native_fn_02008d78(M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x84) + 0x34E, 0, 6);
    native_fn_02008d78(native_data_ov001_022399b8, 0, 0x50);
    M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x2B) = 0;
    M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x29) = 0;
    M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0;
    return (u32) native_data_ov001_0223989c;
}
