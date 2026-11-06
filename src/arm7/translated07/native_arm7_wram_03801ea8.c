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
extern u32 native_arm7_fn_037fe410(u32, u32, u32);
u32 native_arm7_wram_03801ea8(u32 arg0) {
    s32 temp_r0;

    do {
        temp_r0 = (s32) native_arm7_fn_037fe410(7U, arg0, 0U);
    } while (temp_r0 < 0);
    return (u32) temp_r0;
}
