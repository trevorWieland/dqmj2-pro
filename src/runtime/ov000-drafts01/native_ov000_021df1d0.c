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
extern u32 native_fn_ov000_021df3bc();
typedef struct {
    u8 unknown_0[0x7c0];
    u8 field_7c0;
} Record_native_data_ov000_0223142c;
extern Record_native_data_ov000_0223142c native_data_ov000_0223142c;
u32 native_ov000_021df1d0(void) {
    return M2C_FIELD((void *) native_fn_ov000_021df3bc(native_data_ov000_0223142c.field_7c0), u8 *, 0xB) & 1;
}
