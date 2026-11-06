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
extern u32 native_fn_02008c14();
extern u32 native_data_020dd60c[];
extern u32 native_data_020dd610[];
extern u32 native_data_020dd614[];
u32 native_main_0202e958(u32 arg0, u32 arg1) {
    native_fn_02008c14(0U, arg0, 0x54U);
    M2C_FIELD(arg0, s32 *, 0xC) = (s32) *native_data_020dd614;
    M2C_FIELD(arg0, s32 *, 0x14) = (s32) *native_data_020dd610;
    M2C_FIELD(arg0, u32 *, 0x1C) = (u32) *native_data_020dd60c;
    M2C_FIELD(arg0, u32 *, 4) = arg1;
    return *native_data_020dd60c;
}
