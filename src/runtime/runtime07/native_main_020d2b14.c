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
extern u32 native_fn_02061c1c();
extern u32 native_fn_020d2814();
extern u32 native_fn_020d2860();
extern u8 native_data_021d7098[];
u32 native_main_020d2b14(void) {
    native_fn_02061c1c(6, 1, 1, 0xE, 2, 0, 0);
    native_fn_02061c1c(8, 1, 3, 0x15, 2, 0, 0);
    native_fn_02061c1c(7, 0x12, 1, 0xA, 2, 0, 0);
    native_fn_02061c1c(0xF, 8, 5, 7, 2, 0, 0);
    native_fn_02061c1c(0x10, 0x13, 5, 7, 2, 0, 0);
    native_fn_02061c1c(9, 8, 7, 9, 2, 0, 0);
    native_fn_02061c1c(0xA, 0x13, 7, 7, 2, 0, 0);
    native_fn_02061c1c(0xB, 8, 9, 9, 2, 0, 0);
    native_fn_02061c1c(0xC, 0x13, 9, 7, 2, 0, 0);
    native_fn_02061c1c(0xD, 8, 0xB, 0xA, 2, 0, 0);
    native_fn_02061c1c(0xE, 0x13, 0xB, 7, 2, 0, 0);
    native_fn_02061c1c(0x11, 1, 0xD, 0xC, 2, 0, 0);
    native_fn_02061c1c(0x12, 0x13, 0xD, 5, 2, 0, 0);
    native_fn_02061c1c(0x13, 0x19, 0xD, 5, 2, 0, 0);
    native_fn_02061c1c(0x14, 1, 0xF, 0xA, 2, 0, 0);
    native_fn_02061c1c(0x15, 0x13, 0xF, 5, 2, 0, 0);
    native_fn_02061c1c(0x16, 1, 0x11, 9, 2, 0, 0);
    native_fn_02061c1c(0x17, 0x13, 0x11, 7, 2, 0, 0);
    native_fn_02061c1c(0x1A, 1, 0x15, 0xB, 2, 0, 0);
    native_fn_020d2814(0x1B, M2C_FIELD(native_data_021d7098, u16 *, 0x20));
    native_fn_02061c1c(0x18, 1, 0x13, 7, 2, 0, 0);
    return native_fn_020d2860(0x19, M2C_FIELD(native_data_021d7098, s32 *, 0x24));
}
