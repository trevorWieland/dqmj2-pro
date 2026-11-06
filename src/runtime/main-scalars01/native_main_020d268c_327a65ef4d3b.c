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
extern u32 native_fn_0204540c();
extern u32 native_fn_02045770();
extern u32 native_fn_02048f6c();
extern u32 native_fn_020d2614();
extern u32 native_fn_020d2660();
extern u8 native_data_021d70d8[];
extern u8 native_data_021d70dc[];
u32 native_main_020d268c(u32 arg0, s32 arg1, s32 arg2) {
    u32 temp_r4;

    temp_r4 = native_fn_02048f6c(0);
    native_fn_020d2614();
    native_fn_020d2660(native_data_021d70d8, arg0);
    native_fn_0204540c(temp_r4, native_data_021d70dc, 0x7F80, 0x80);
    return native_fn_02045770(0, temp_r4, 2, 2, arg1, arg2, 0x20, 0x3FC, *(u32 *)native_data_021d70d8 + 2);
}
