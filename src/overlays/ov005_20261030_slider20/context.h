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
#define NULL ((void *)0)
extern u32 native_fn_02048a44();
extern u32 native_fn_02048a60();
typedef struct {
    u8 unknown_0[0x2c];
    s32 field_2c;
    u8 unknown_30[0x10];
    s32 field_40;
    u8 unknown_44[0x24];
    s32 field_68;
} Record_native_data_ov005_021e9818;
extern Record_native_data_ov005_021e9818 native_data_ov005_021e9818;
typedef struct {
    u8 unknown_0[0x7c];
    s32 field_7c;
} Record_native_data_ov005_021e9a28;
extern Record_native_data_ov005_021e9a28 native_data_ov005_021e9a28;
extern u8 native_data_ov005_021e9ab8[];
typedef struct {
    u8 unknown_0[0x7c];
    s32 field_7c;
} Record_native_data_ov005_021e9b48;
extern Record_native_data_ov005_021e9b48 native_data_ov005_021e9b48;
extern u8 native_data_ov005_021e9bd8[];
extern u8 native_data_ov005_021e9cf8[];
extern u8 native_data_ov005_021e9ea8[];
extern u8 native_data_ov005_021e9eb0[];
extern u8 native_data_ov005_021e9f38[];
extern u8 native_data_ov005_021ea0e8[];
extern u8 native_data_ov005_021ea298[];
