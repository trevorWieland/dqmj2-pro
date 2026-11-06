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
extern u32 native_fn_ov000_0204bd6c(u32);
extern u32 native_data_ov000_02233ae8;
u32 native_ov000_021e52c0(void) {
    return native_fn_ov000_0204bd6c((u32) &native_data_ov000_02233ae8);
}
