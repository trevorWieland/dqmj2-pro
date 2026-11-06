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
extern u32 native_fn_01ffb35c();
extern u32 native_fn_0205e7a8();
u32 native_main_020894e0(void) {
    u16 temp_r0;

    if (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 1) {
        return native_fn_0205e7a8(-1, 0x52);
    }
    temp_r0 = M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2);
    if (!(temp_r0 & 2)) {
        return (u32) temp_r0;
    }
    return native_fn_0205e7a8(-1, 0x53);
}
