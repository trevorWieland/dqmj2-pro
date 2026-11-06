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
extern u32 native_fn_ov000_02206724(u32);
extern u32 native_data_ov000_022383bc;
u32 native_ov000_022078cc(void) {
    return native_fn_ov000_02206724((u32) &native_data_ov000_022383bc);
}
