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
extern u32 native_fn_020baf04();
extern u8 native_data_ov006_0220f594[];
extern u8 native_data_ov006_0220f828[];
extern u8 native_data_ov006_0220f834[];
u32 native_ov006_021df974(s32 arg0, s32 arg1, u8 *arg2, s32 arg3) {
    M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x3C) = arg0;
    M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x28) = arg1;
    M2C_FIELD(native_data_ov006_0220f594, u8 **, 0x30) = arg2;
    M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x20) = arg3;
    M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x38) = 0;
    M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x34) = -1;
    M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x10) = 0;
    M2C_FIELD(native_data_ov006_0220f594, s32 *, 0xC) = 0;
    M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x48) = 1;
    if (arg0 == 2) {
        native_fn_020baf04(native_data_ov006_0220f828);
        native_fn_02008e0c(M2C_FIELD(native_data_ov006_0220f594, u8 **, 0x30), native_data_ov006_0220f834, M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x20));
        M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x20) = (s32) (M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x20) + 0xC);
        M2C_FIELD(native_data_ov006_0220f594, u8 **, 0x30) = native_data_ov006_0220f828;
    }
    if (M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x3C) == 1) {
        M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x20) = (s32) (M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x20) + 0xC);
    }
    M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x14) = 0;
    M2C_FIELD(native_data_ov006_0220f594, s32 *, 0x44) = 5;
    return (u32) native_data_ov006_0220f594;
}
