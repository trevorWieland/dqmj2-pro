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
extern u32 native_fn_02048f8c();
extern u32 native_fn_020620b4();
extern u32 native_fn_02062358();
extern u32 native_fn_020625ac();
extern u32 native_fn_0206dc70();
extern u32 native_fn_020c1708();
extern u32 native_fn_020c17e8();
extern u32 native_fn_020c4220();
extern u32 native_fn_020cc740();
extern u32 native_fn_020cc75c();
extern u32 native_fn_020cca0c();
extern u32 native_fn_020ccb3c();
extern u32 native_fn_020cd1ac();
extern u32 native_fn_020cd314();
u32 native_main_020cd9d4(void) {
    s32 sp0;

    native_fn_020cd1ac(native_fn_020cc740(), 0);
    native_fn_020cc740();
    native_fn_020cd314();
    native_fn_020cca0c();
    native_fn_020c17e8(0, 0);
    sp0 = -1;
    native_fn_020c1708(&sp0);
    native_fn_020c4220(0xB, native_fn_02048f8c(1));
    native_fn_020ccb3c(1);
    if (native_fn_020cc75c() == 6) {
        native_fn_020625ac(1);
    }
    native_fn_0206dc70();
    native_fn_020620b4(1);
    return native_fn_02062358(1);
}
