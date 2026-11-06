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
extern u32 native_fn_02009200();
extern u32 native_fn_020097b8();
extern u32 native_fn_02009974();
extern u32 native_fn_020099e0();
extern u32 native_fn_020378d8();
void native_main_02037fac(void) {
    u32 temp_r4;

    native_fn_020378d8();
    native_fn_02009200(0, 0, 0, 0);
    temp_r4 = native_fn_020099e0();
    native_fn_020097b8(1);
    native_fn_02009974(temp_r4);
}
