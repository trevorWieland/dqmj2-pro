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
extern u32 native_fn_020456ac();
extern u32 native_fn_02048f6c();
extern u32 native_fn_02061d08();
extern u32 native_fn_020643fc();
extern u32 native_fn_020d268c();
extern u32 native_fn_020d2860();
extern u32 native_fn_020d2e68();
extern u8 native_data_021d7098[];
u32 native_main_020d3428(void) {
    native_fn_020456ac(0, native_fn_02048f6c(0), 0x10, 1, 2, 2);
    native_fn_020d268c(native_fn_020643fc(M2C_FIELD(native_data_021d7098, u16 *, 0x22)), 0x10, 1);
    native_fn_02061d08(0x19, 0);
    native_fn_020d2860(0x19, M2C_FIELD(native_data_021d7098, s32 *, 0x24));
    return native_fn_020d2e68();
}
