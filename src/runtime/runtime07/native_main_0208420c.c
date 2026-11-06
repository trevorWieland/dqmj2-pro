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
extern u32 native_fn_020142d8();
extern u32 native_fn_0208455c();
extern u8 native_data_021c9600[];
u32 native_main_0208420c(void) {
    M2C_FIELD(native_data_021c9600, s32 *, 0x10) = 1;
    M2C_FIELD(native_data_021c9600, s16 *, 4) = (s16) native_fn_0208455c();
    return native_fn_020142d8(0, 0);
}
