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
extern u32 native_fn_02005b38();
extern u32 native_fn_02005dac();
extern u32 native_fn_02005de0();
extern u32 native_fn_02006498();
extern u32 native_fn_02007360();
extern u32 native_fn_020073c8();
extern u32 native_fn_020074cc();
extern u32 native_fn_0200776c();
extern u32 native_fn_02007f98();
extern u32 native_fn_0200808c();
extern u32 native_fn_020082a4();
extern u32 native_fn_020090a8();
extern u32 native_fn_0200a2c4();
extern u32 native_fn_0200e504();
extern u32 native_fn_02011194();
extern u32 native_fn_020194b4();
void native_main_02007380(void) {
    native_fn_020073c8();
    native_fn_0200a2c4();
    native_fn_02005de0();
    native_fn_020074cc();
    native_fn_02005b38();
    native_fn_02005dac();
    native_fn_0200776c();
    native_fn_020090a8();
    native_fn_02007f98();
    native_fn_020082a4();
    native_fn_02006498();
    native_fn_0200808c();
    native_fn_020194b4();
    native_fn_02011194();
    native_fn_0200e504();
    native_fn_02007360();
}
