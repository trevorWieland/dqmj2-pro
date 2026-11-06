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
extern u32 native_fn_0205e7a8(u32 arg0, u32 arg1);
extern u32 native_fn_0207f4bc(u32 arg0);
extern u32 native_fn_02081aec(u8);
extern u8 native_data_021c6e50;

u32 native_main_02081b30(void) {
    u8 temp_r2;

    if (native_data_021c6e50 == 0) {
        native_fn_0205e7a8(-1U, 0x54U);
        native_data_021c6e50 = 0;
    } else {
        native_fn_02081aec(--native_data_021c6e50);
        native_fn_0205e7a8(-1U, 0x53U);
    }
    native_fn_0207f4bc(1U);
    return 0U;
}
