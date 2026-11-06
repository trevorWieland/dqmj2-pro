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
extern u32 native_fn_020655b8();
typedef struct {
    u8 unknown_0[0x6];
    s8 field_6;
    u8 unknown_7[0x1];
    s8 field_8;
    u8 unknown_9[0x2b];
    s16 field_34;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
void native_ov001_021dd14c(void) {
    native_data_ov001_022388ec.field_34 = (s16) native_fn_020655b8();
    native_data_ov001_022388ec.field_8 = 0;
    native_data_ov001_022388ec.field_6 = 0;
}
