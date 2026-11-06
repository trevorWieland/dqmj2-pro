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
extern u32 native_fn_020090c0();
extern u32 native_fn_02009148();
extern u32 native_fn_020387a8();
void native_main_02038708(void *arg0) {
    if (M2C_FIELD(arg0, u8 *, 0x2C) == 2) {
        native_fn_02009148(M2C_FIELD(arg0, u8 *, 0x3C), 0xFFFFFD2D);
    }
    native_fn_020090c0(M2C_FIELD(arg0, u8 *, 0x3C));
    native_fn_020387a8(arg0);
}
