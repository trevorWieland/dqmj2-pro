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
extern u32 native_fn_02045490();
extern u32 native_fn_0204b078();
u32 native_main_0204ac5c(u32 arg0, s32 arg1, u32 arg2, u32 arg3, s32 arg4) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r0 = native_fn_0204b078(arg0, 0, arg3);
    if (temp_r0 == 0) {
        return 0U;
    }
    temp_r4 = (M2C_FIELD(temp_r0, u8 *, 0) * M2C_FIELD(temp_r0, u8 *, 2)) << 5;
    if (arg1 == 0) {
        native_fn_0204540c(arg2, temp_r0 + 4, arg4, temp_r4);
    } else {
        native_fn_02045490(arg2, temp_r0 + 4, arg4, temp_r4);
    }
    return temp_r4;
}
