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
extern u32 native_fn_0205dfd8();
extern u32 native_fn_0205e6c4();
extern u32 native_fn_0205f5dc();
extern u8 native_data_02106950[];
u32 native_main_0205e408(void) {
    u32 temp_r0;

    native_fn_0205dfd8(0);
    native_fn_0205e6c4();
    temp_r0 = native_fn_0205f5dc();
    M2C_FIELD(native_data_02106950, u32 *, 8) = temp_r0;
    M2C_FIELD(native_data_02106950, s8 *, 1) = 0;
    return temp_r0;
}
