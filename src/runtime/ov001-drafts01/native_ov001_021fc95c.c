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
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u8 native_data_ov001_0222ed34[];
typedef struct {
    u8 unknown_0[0x20];
    s32 field_20;
    s32 field_24;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
u32 native_ov001_021fc95c(void) {
    native_fn_020485b4(native_data_ov001_02239c10.field_20);
    native_fn_020484dc(1, *native_data_ov001_0222ed34);
    native_data_ov001_02239c10.field_20 = 0;
    native_data_ov001_02239c10.field_24 = 0;
    *native_data_ov001_0222ed34 = 0x7F;
    return (u32) native_data_ov001_0222ed34;
}
