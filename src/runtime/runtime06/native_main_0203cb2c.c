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
extern u32 native_fn_02003af4();
extern u32 native_fn_02003b08();
extern u32 native_fn_02003b1c();
extern u32 native_fn_02003b40();
extern u32 native_fn_02003b64();
extern u32 native_fn_02003b78();
extern u32 native_fn_02003cf8();
extern u32 native_fn_02003d0c();
extern u32 native_fn_02003d20();
extern u32 native_fn_02003d44();
extern u32 native_fn_02003d68();
extern u32 native_fn_02003d7c();
void native_main_0203cb2c(void) {
    native_fn_02003b64();
    native_fn_02003b08();
    native_fn_02003af4();
    native_fn_02003b78();
    native_fn_02003b1c();
    native_fn_02003b40();
    native_fn_02003cf8();
    native_fn_02003d0c();
    native_fn_02003d68();
    native_fn_02003d20();
    native_fn_02003d44();
    native_fn_02003d7c();
}
