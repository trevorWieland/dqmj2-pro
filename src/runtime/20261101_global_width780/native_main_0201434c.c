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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_02008e0c();
extern u32 native_fn_020156cc();
extern u32 native_data_020ec36c[];
u32 native_main_0201434c(u32 arg0) {
    u32 temp_r4;

    temp_r4 = native_fn_02007ff4();
    if ((*native_data_020ec36c != 0) && (native_fn_020156cc(arg0) != 0)) {
        native_fn_02008e0c(((arg0 - 1) * 0x16) + (*native_data_020ec36c + 0x1340), *native_data_020ec36c + 0x1772, 0x16U, *native_data_020ec36c);
        native_fn_02008008(temp_r4);
        return *native_data_020ec36c + 0x1772;
    }
    native_fn_02008008(temp_r4);
    return 0U;
}
