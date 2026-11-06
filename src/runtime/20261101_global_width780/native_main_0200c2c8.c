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
extern u32 native_fn_020102c4();
extern u32 native_fn_020102e0();
extern u32 native_data_020e535c[];
u32 native_main_0200c2c8(u32 arg0, u32 arg1) {
    switch (arg1) {
    case 9:
        native_fn_020102c4((u32) (u16) *native_data_020e535c);
        return 0U;
    case 10:
        native_fn_020102e0((u32) (u16) *native_data_020e535c);
        return 0U;
    case 1:
        return 4U;
    default:
        return 8U;
    }
}
