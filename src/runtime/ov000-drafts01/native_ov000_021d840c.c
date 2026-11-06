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
extern u32 native_fn_02008c58();
extern u32 native_fn_02028264();
extern u32 native_fn_02028280();
extern u32 native_fn_020282a8();
extern u32 native_fn_0202834c();
extern u32 native_fn_0202838c();
extern u32 native_fn_020283b4();
extern u32 native_fn_0202841c();
extern u32 native_fn_ov000_021d8378();
extern u32 native_fn_ov000_021d8c80();
extern u8 native_data_ov000_0223033c[];
u32 native_ov000_021d840c(void) {
    native_fn_02008c58(0, native_data_ov000_0223033c, 0xAC);
    native_fn_02028264(native_data_ov000_0223033c);
    native_fn_02028280(native_data_ov000_0223033c);
    M2C_FIELD(native_data_ov000_0223033c, s32 *, 0x98) = 0;
    native_fn_ov000_021d8c80(1);
    M2C_FIELD(native_data_ov000_0223033c, s32 *, 0x4C) = (s32) M2C_FIELD(native_data_ov000_0223033c, s32 *, 0x98);
    M2C_FIELD(native_data_ov000_0223033c, s32 *, 0x50) = (s32) M2C_FIELD(native_data_ov000_0223033c, s32 *, 0x9C);
    M2C_FIELD(native_data_ov000_0223033c, s32 *, 0x54) = (s32) M2C_FIELD(native_data_ov000_0223033c, s32 *, 0xA0);
    M2C_FIELD(native_data_ov000_0223033c, s32 *, 0x58) = (s32) M2C_FIELD(native_data_ov000_0223033c, s32 *, 0xA4);
    M2C_FIELD(native_data_ov000_0223033c, s8 *, 0xA8) = 1;
    native_fn_020282a8(0, 0x1E000);
    native_fn_0202834c(0, 0x1555);
    native_fn_0202838c(0, 0x333);
    native_fn_020283b4(0, 0x5DC000);
    native_fn_0202841c(0, 0);
    return native_fn_ov000_021d8378();
}
