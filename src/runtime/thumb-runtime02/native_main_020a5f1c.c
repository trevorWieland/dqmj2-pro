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
extern u32 native_fn_020a5ef8();
extern u32 native_fn_020a5f04();
extern u32 native_fn_020a5f10();
extern u32 native_fn_020a88ec();
extern u8 native_data_021d2360[];
u32 native_main_020a5f1c(void) {
    if (M2C_FIELD(native_data_021d2360, u32 *, 4) == 0) {
        M2C_FIELD(native_data_021d2360, u32 *, 4) = native_fn_020a88ec(8, 0x64, 2, native_fn_020a5ef8, native_fn_020a5f04, native_fn_020a5f10);
    }
    return M2C_FIELD(native_data_021d2360, u32 *, 4);
}
