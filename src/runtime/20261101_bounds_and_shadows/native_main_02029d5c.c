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
typedef struct {
    u8 unknown_0[0x18];
    u16 field_18;
} Record_native_data_020edd0c;
extern Record_native_data_020edd0c native_data_020edd0c;
u32 native_main_02029d5c(u32 arg0) {
    u16 temp_r0;
    u16 temp_r3;

    temp_r0 = native_data_020edd0c.field_18;
    temp_r3 = (u16) arg0;
    native_data_020edd0c.field_18 = temp_r3;
    *(u16 *)0x04000354 = temp_r3;
    return (u32) temp_r0;
}
