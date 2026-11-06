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
extern u32 native_fn_02085270();
extern u32 native_fn_02085284();
extern u32 native_fn_02086b14();
extern u8 native_data_02102974[];
u32 native_main_02049e28(u32 arg0, u32 arg1, u32 arg2) {
    void *temp_r4;

    temp_r4 = M2C_FIELD(native_data_02102974, void **, 0x10);
    native_fn_02085270(temp_r4 + 0x3C, 0, 0);
    native_fn_02085284(temp_r4 + 0x3C, arg0, arg1, arg2);
    M2C_FIELD(temp_r4, s32 *, 0x18) = (s32) (M2C_FIELD(temp_r4, s32 *, 0x18) | 2);
    return native_fn_02086b14(temp_r4, 0xA);
}
