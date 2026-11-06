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
typedef struct {
    u8 field_0;
    u8 field_1;
    u8 field_2;
    u8 field_3;
} Record_native_data_ov001_022355e4;
extern Record_native_data_ov001_022355e4 native_data_ov001_022355e4;
u32 native_ov001_021db530(s32 arg0) {
    if (arg0 == 0) {
        return (u32) native_data_ov001_022355e4.field_3;
    }
    else if (arg0 == 1) {
        return (u32) native_data_ov001_022355e4.field_2;
    }
    else if (arg0 == 2) {
        return (u32) native_data_ov001_022355e4.field_0;
    }
    else if (arg0 == 3) {
        return (u32) native_data_ov001_022355e4.field_1;
    }
    else {
        return -1U;
    }

}
