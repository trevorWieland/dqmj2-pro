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
extern u32 native_fn_01ffc2c0();
extern u32 native_fn_01ffc2c8();
extern u32 native_fn_01ffc2d0();
extern u32 native_fn_01ffc2d4();
extern u32 native_fn_020ba7c4();
u32 native_itcm_01ffc2dc(void) {
    return native_fn_020ba7c4(2, native_fn_01ffc2c0, native_fn_01ffc2c8, native_fn_01ffc2d0, native_fn_01ffc2d4, 0x1388);
}
