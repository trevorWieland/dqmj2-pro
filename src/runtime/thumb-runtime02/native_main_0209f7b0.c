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
extern u32 native_fn_0209aa64();
extern u32 native_fn_020a2ac8();
extern u32 native_fn_020a3d64();
extern u8 native_data_021d1b88[];
u32 native_main_0209f7b0(void) {
    native_fn_020a3d64(0);
    if (M2C_FIELD(native_data_021d1b88, s32 *, 8) != 0) {
        native_fn_0209aa64(4, M2C_FIELD(native_data_021d1b88, s32 *, 8), 0);
        M2C_FIELD(native_data_021d1b88, s32 *, 8) = 0;
    }
    native_fn_020a2ac8();
    if (M2C_FIELD(native_data_021d1b88, s32 *, 0) != 0) {
        native_fn_0209aa64(4, M2C_FIELD(native_data_021d1b88, s32 *, 0), 0);
        M2C_FIELD(native_data_021d1b88, s32 *, 0) = 0;
    }
    M2C_FIELD(native_data_021d1b88, s8 *, 0x1C) = 0;
    M2C_FIELD(native_data_021d1b88, s8 *, 0x1D) = 0;
    return (u32) native_data_021d1b88;
}
