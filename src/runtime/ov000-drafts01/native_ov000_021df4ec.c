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
extern u8 native_data_ov000_02231c04[];
extern u8 native_data_ov000_02231d24[];
extern u8 native_data_ov000_02231e44[];
extern u8 native_data_ov000_02231f64[];
u32 native_ov000_021df4ec(void) {
    native_fn_02008c14(0, native_data_ov000_02231f64, 0x300);
    native_fn_02008c14(0, native_data_ov000_02231e44, 0x120);
    native_fn_02008c14(0, native_data_ov000_02231c04, 0x120);
    return native_fn_02008c14(0, native_data_ov000_02231d24, 0x120);
}
