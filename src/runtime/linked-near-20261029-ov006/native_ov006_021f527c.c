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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02002c14();
extern u32 native_fn_0200f0a4();
extern u32 native_fn_ov006_021ff6b4();
extern u32 native_fn_ov006_022029ac();
extern u32 native_fn_ov006_02202c1c();
extern u32 native_fn_ov006_02203178();
extern u32 native_fn_ov006_022033ec();
extern u32 native_fn_ov006_02203bc0();
extern u32 native_fn_ov006_02203cc8();
extern u32 native_fn_ov006_022041f0();
extern u32 native_fn_ov006_02204364();
extern u32 native_fn_ov006_02204684();
extern u32 native_fn_ov006_022047c8();
extern u32 native_fn_ov006_02204874();
u32 native_ov006_021f527c(void) {
    native_fn_02002c14();
    *(s32 *)0x04001000 &= 0xFFFEFFFF;
    native_fn_ov006_022047c8();
    native_fn_0200f0a4(1);
    native_fn_ov006_02203cc8();
    native_fn_ov006_022041f0();
    native_fn_ov006_021ff6b4();
    native_fn_ov006_02202c1c();
    native_fn_ov006_02204364();
    native_fn_ov006_022033ec();
    native_fn_ov006_02203178();
    native_fn_ov006_022029ac();
    native_fn_ov006_02204874();
    native_fn_ov006_02203bc0();
    return native_fn_ov006_02204684();
}
