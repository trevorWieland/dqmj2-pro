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
extern u32 native_fn_020061ac();
extern u8 native_data_020e01f4[];
extern u8 native_data_020e01fc[];
extern u8 native_data_020e0208[];
extern u8 native_data_020e0214[];
extern u8 native_data_020e0240[];
u32 native_main_0209fda4(u32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    return native_fn_020061ac(arg0, 0x100, native_data_020e0240, native_data_020e0214, 3, native_data_020e01f4, arg1, arg2, arg2, native_data_020e01fc, arg3, native_data_020e0208, native_data_020e01f4);
}
