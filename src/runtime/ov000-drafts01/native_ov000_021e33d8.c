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
extern u32 native_fn_02008c14();
extern u8 native_data_ov000_02232568[];
extern u8 native_data_ov000_02232668[];
extern u8 native_data_ov000_02232868[];
extern u8 native_data_ov000_02232ae8[];
extern u8 native_data_ov000_022332e8[];
u32 native_ov000_021e33d8(void) {
    native_fn_02008c14(0, native_data_ov000_02232868, 0x280);
    native_fn_02008c14(0, native_data_ov000_022332e8, 0x800);
    native_fn_02008c14(0, native_data_ov000_02232ae8, 0x800);
    native_fn_02008c14(0, native_data_ov000_02232668, 0x200);
    return native_fn_02008c14(0, native_data_ov000_02232568, 0x200);
}
