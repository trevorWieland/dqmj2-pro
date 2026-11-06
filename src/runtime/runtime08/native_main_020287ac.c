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
u32 native_main_020287ac(void *arg0, s32 arg1, s32 arg2, s32 arg3) {
    u16 temp_ip;

    temp_ip = M2C_FIELD(arg0, u16 *, 0xE);
    M2C_FIELD(arg0, u16 *, 0xE) = (u16) (arg1 | (arg2 << 5) | (arg3 << 0xA));
    return (u32) temp_ip;
}
