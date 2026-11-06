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
extern u32 native_fn_020065f0();
extern u32 native_fn_0200698c();
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_02019898();
extern u32 native_fn_020198ac();
extern u32 native_data_020ec588[];
extern u8 native_data_020ec58c[];
extern u8 native_data_020ec9b0[];
u32 native_main_0201980c(u32 arg0) {
    u32 temp_r4;

    temp_r4 = native_fn_02007ff4();
    if (*native_data_020ec588 == 0) {
        *native_data_020ec588 = arg0;
        native_fn_02019898(arg0 + 0xC4);
        native_fn_02019898((u32) native_data_020ec58c);
        M2C_FIELD(arg0, s32 *, 0xC0) = 0;
        native_fn_020065f0(arg0, native_fn_020198ac, arg0, native_data_020ec9b0, 0x400, 0x14);
        native_fn_0200698c((void *) arg0);
    }
    return native_fn_02008008(temp_r4);
}
