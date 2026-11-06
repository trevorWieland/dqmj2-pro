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
extern u32 native_fn_0203c06c();
extern u32 native_fn_0203c08c();
u32 native_main_0203c3a0(void *arg0) {
    if (native_fn_0203c08c() != 0) {
        return 0U;
    }
    M2C_FIELD(arg0, u16 *, 0xA) = (u16) native_fn_0203c06c(arg0, M2C_FIELD(arg0, u16 *, 0xA));
    M2C_FIELD(arg0, u16 *, 0xC) = (u16) (M2C_FIELD(arg0, u16 *, 0xC) + 1);
    return 1U;
}
