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
extern u32 native_fn_02029d84();
extern u32 native_fn_ov000_021dfe0c();
extern u32 native_fn_ov000_021dfe5c();
extern u32 native_fn_ov000_021dfe80();
extern u32 native_fn_ov000_021dfea4();
u32 native_ov000_022146c0(void) {
    native_fn_ov000_021dfe0c();
    native_fn_ov000_021dfe5c(0, 0xA58, -0xA20, -0x6C0);
    native_fn_ov000_021dfe80(0, 0x17, 0x17, 0x17);
    native_fn_ov000_021dfea4(0, 1);
    native_fn_ov000_021dfe5c(1, 0xBA8, 0x328, -0xA78);
    native_fn_ov000_021dfe80(1, 0xE, 0xE, 0xE);
    native_fn_ov000_021dfea4(1, 1);
    native_fn_ov000_021dfe5c(2, 0xFFFFF6D8, -0xAB8, 0xFFFFF880);
    native_fn_ov000_021dfe80(2, 8, 8, 8);
    native_fn_ov000_021dfea4(2, 1);
    native_fn_ov000_021dfe5c(3, -0x6C0, 0x258, 0xE50);
    native_fn_ov000_021dfe80(3, 4, 4, 4);
    native_fn_ov000_021dfea4(3, 1);
    return native_fn_02029d84(0);
}
