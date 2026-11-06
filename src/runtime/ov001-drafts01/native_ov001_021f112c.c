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
extern u32 native_fn_02048404();
extern u32 native_fn_0204854c();
extern u8 native_data_ov001_0222ecb0[];
extern u8 native_data_ov001_0222ecc8[];
extern u8 native_data_ov001_0222ece0[];
extern u8 native_data_ov001_0222ecfc[];
typedef struct {
    u8 field_0;
    u8 unknown_1[0xb];
    u32 field_c;
    u32 field_10;
} Record_native_data_ov001_02238f58;
extern Record_native_data_ov001_02238f58 native_data_ov001_02238f58;
u32 native_ov001_021f112c(u8 arg0) {
    u32 temp_r0;
    u32 temp_r0_2;

    native_data_ov001_02238f58.field_0 = arg0;
    switch (arg0) {
    case 0:
        *native_data_ov001_0222ecb0 = (u8) native_fn_02048404(0, native_data_ov001_0222ecc8, 4, 2);
        break;
    case 1:
        *native_data_ov001_0222ecb0 = (u8) native_fn_02048404(0, native_data_ov001_0222ece0, 4, 2);
        break;
    case 2:
        *native_data_ov001_0222ecb0 = (u8) native_fn_02048404(0, native_data_ov001_0222ecfc, 4, 2);
        break;
    }
    temp_r0_2 = native_fn_0204854c(0, *native_data_ov001_0222ecb0);
    native_data_ov001_02238f58.field_c = temp_r0_2;
    temp_r0 = M2C_FIELD(temp_r0_2, u32 *, 4);
    native_data_ov001_02238f58.field_10 = temp_r0;
    return temp_r0;
}
