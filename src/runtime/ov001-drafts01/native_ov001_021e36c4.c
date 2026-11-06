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
extern u32 native_fn_0201d444();
extern u32 native_fn_ov001_021d732c();
extern u32 native_fn_ov001_021d7564();
extern u32 native_fn_ov001_021d7d4c();
extern u8 native_data_ov001_0222ec44[];
extern u8 native_data_ov001_0222ec4c[];
extern u8 native_data_ov001_0222ec54[];
u32 native_ov001_021e36c4(u32 arg0, u32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    u8 sp0[20];

    native_fn_ov001_021d732c(arg0, 2);
    if (arg2 != 0) {
        native_fn_0201d444(&sp0, native_fn_ov001_021d7d4c(arg2));
    } else if (arg3 != 0) {
        native_fn_0201d444(&sp0, (u32) native_data_ov001_0222ec44);
    } else if (arg4 != 0) {
        native_fn_0201d444(&sp0, (u32) native_data_ov001_0222ec4c);
    } else {
        native_fn_0201d444(&sp0, (u32) native_data_ov001_0222ec54);
    }
    return native_fn_ov001_021d7564(arg0, &sp0, arg1);
}
