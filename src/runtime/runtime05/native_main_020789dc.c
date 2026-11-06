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
extern u32 native_fn_020620b4();
extern u32 native_fn_02062a50();
extern u32 native_fn_0206b324();
extern u32 native_fn_0206b35c();
extern u32 native_fn_0206c140();
extern u32 native_fn_0206dcd0();
extern u32 native_fn_02078cbc();
extern u32 native_fn_02078e88();
extern u32 native_fn_ov000_022179fc();
extern u32 native_fn_ov000_02217dbc();
u32 native_main_020789dc(void) {
    native_fn_02078cbc();
    native_fn_02078e88();
    native_fn_02062a50(0);
    native_fn_0206dcd0();
    native_fn_020620b4(1);
    native_fn_ov000_022179fc();
    native_fn_0206b324(0);
    native_fn_ov000_02217dbc();
    native_fn_0206b35c();
    native_fn_0206c140();
    return 0U;
}
