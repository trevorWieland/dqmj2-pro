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
extern u32 native_fn_0202a634(void);
extern u32 native_fn_02044424(u32 arg0);
extern u32 native_fn_ov001_021dcb44(void);
extern u32 native_fn_ov001_021e8748(void);
extern u32 native_fn_ov001_021f165c(void);
extern u32 native_fn_ov001_021f1798(void);
extern u32 native_fn_ov001_0220b6c4(void);
extern u32 native_fn_ov001_02210dd0(void);
extern u32 native_fn_ov001_02210e08(void);
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
typedef char Field_1_LayoutCheck[((u32)&((Record_native_data_ov001_022388ec*)0)->field_1==0x1)?1:-1];
typedef char Field_5_LayoutCheck[((u32)&((Record_native_data_ov001_022388ec*)0)->field_5==0x5)?1:-1];
typedef char Field_6_LayoutCheck[((u32)&((Record_native_data_ov001_022388ec*)0)->field_6==0x6)?1:-1];
typedef char Field_8_LayoutCheck[((u32)&((Record_native_data_ov001_022388ec*)0)->field_8==0x8)?1:-1];
typedef char Field_9_LayoutCheck[((u32)&((Record_native_data_ov001_022388ec*)0)->field_9==0x9)?1:-1];
typedef char Field_38_LayoutCheck[((u32)&((Record_native_data_ov001_022388ec*)0)->field_38==0x38)?1:-1];
