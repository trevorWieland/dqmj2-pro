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
extern u32 native_fn_020a8c34();
extern u32 native_fn_020a8ef8();
extern u8 native_data_021d2470[];
extern u8 native_data_021d2474[];
extern u8 native_data_021d247c[];
u32 native_main_020a92f8(void) {
    u32 temp_r0;

    native_fn_020a8c34(M2C_FIELD(native_data_021d2470, s32 *, 0), native_data_021d247c, M2C_FIELD(native_data_021d2470, s32 *, 0x4C), 0, native_data_021d2474, 8);
    temp_r0 = native_fn_020a8ef8();
    M2C_FIELD(native_data_021d2470, u32 *, 0x50) = temp_r0;
    return temp_r0;
}
