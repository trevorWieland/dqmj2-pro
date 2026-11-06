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
extern u32 native_fn_0209d704();
extern u32 native_fn_020aa1d0();
extern u8 native_data_020e0188[];
extern u8 native_data_021d1b74[];
u32 native_main_0209d66c(u32 arg0) {
    u32 temp_r4;

    temp_r4 = native_fn_020aa1d0(M2C_FIELD(M2C_FIELD(native_data_021d1b74, void **, 0xC), s32 *, 4), arg0, native_data_020e0188);
    native_fn_0209d704();
    return temp_r4;
}
