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
extern u32 native_fn_02085318();
extern u32 native_fn_02086b14();
u32 native_main_020854c8(void *arg0) {
    M2C_FIELD(arg0, s8 *, 0x36) = (s8) ((s32) (M2C_FIELD(arg0, u8 *, 0x1E) + 0x10) >> 4);
    M2C_FIELD(arg0, s8 *, 0x37) = (s8) ((s32) (M2C_FIELD(arg0, u8 *, 0x1F) + 0x10) >> 4);
    M2C_FIELD(arg0, s8 *, 0x32) = (s8) (M2C_FIELD(arg0, u8 *, 0x1C) + ((s32) M2C_FIELD(arg0, u8 *, 0x1E) >> 1));
    M2C_FIELD(arg0, s8 *, 0x33) = (s8) (M2C_FIELD(arg0, u8 *, 0x1D) + ((s32) M2C_FIELD(arg0, u8 *, 0x1F) >> 1));
    M2C_FIELD(arg0, s8 *, 0x34) = 0;
    M2C_FIELD(arg0, s8 *, 0x35) = 0;
    native_fn_02085318(arg0, 8);
    native_fn_02086b14(arg0, 2);
    return 1U;
}
