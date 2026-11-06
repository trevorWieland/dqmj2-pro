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
extern u32 native_fn_0209f80c();
extern u32 native_fn_020a3d70();
extern u32 native_fn_020b85d8();
extern u8 native_data_020e01f4[];
extern u8 native_data_020e01fc[];
extern u8 native_data_020e0208[];
extern u8 native_data_020e0214[];
extern u8 native_data_020e0220[];
u32 native_main_0209fb40(s8 arg0, s8 arg1, s32 arg2, s32 arg3) {
    native_fn_0209f80c(0);
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x15) = arg0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x16) = arg1;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x464) = arg2;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x468) = arg3;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x17D) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x2D0) = 0;
    native_fn_020b85d8(0x32, native_data_020e01f4);
    native_fn_020b85d8(0x33, native_data_020e01fc);
    native_fn_020b85d8(0x34, native_data_020e0208);
    native_fn_020b85d8(0x35, native_data_020e0214);
    return native_fn_020b85d8(0x36, native_data_020e0220);
}
