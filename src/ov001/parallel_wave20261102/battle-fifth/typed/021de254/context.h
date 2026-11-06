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
extern u32 native_fn_0207b6e8();
extern u32 native_fn_0207b748();
extern u32 native_fn_ov001_02216cfc();
extern u32 native_fn_ov001_022170f4();
extern u32 native_fn_ov001_02217910();
extern u32 native_fn_ov001_02217920();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x3];
    s8 field_4;
    u8 unknown_5[0x3];
    s8 field_8;
    u8 unknown_9[0x13];
    s8 field_1c;
    u8 unknown_1d[0x23];
    s32 field_40;
    u8 unknown_44[0x4];
    s32 field_48;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
extern u8 native_data_ov001_02238a08[];
extern u32 native_data_ov001_02238a0c[];
