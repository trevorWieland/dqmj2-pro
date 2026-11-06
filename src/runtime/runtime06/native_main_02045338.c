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
extern u32 native_fn_02008c14();
extern u32 native_fn_02045394();
extern u32 native_fn_02045400();
extern u8 native_data_020f6a0c[];
void native_main_02045338(void) {
    native_fn_02008c14(0, native_data_020f6a0c, 0x18);
    native_fn_02045394();
    native_fn_02045400();
}
