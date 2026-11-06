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
extern u32 native_fn_0202a634();
extern u32 native_fn_02044424();
extern u32 native_fn_ov001_021dcb44();
extern u32 native_fn_ov001_021e8748();
extern u32 native_fn_ov001_021f165c();
extern u32 native_fn_ov001_021f1798();
extern u32 native_fn_ov001_0220b6c4();
extern u32 native_fn_ov001_02210dd0();
extern u32 native_fn_ov001_02210e08();
typedef struct {
    u8 unknown_0[0x1];
    u8 field_1;
    u8 unknown_2[0x3];
    u8 field_5;
    u8 field_6;
    u8 unknown_7[0x1];
    u8 field_8;
    u8 field_9;
    u8 unknown_a[0x2e];
    s32 field_38;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
