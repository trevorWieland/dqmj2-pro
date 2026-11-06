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
extern u32 native_arm7_fn_03806c38(u32, u32, u32, u32);
u32 native_arm7_wram_037ffe64(s32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    if (arg0 == 0x7F) {
        return 0xFFFFU;
    }
    if (arg0 == 0x7E) {
        return 0x3C00U;
    }
    if (arg0 < 0x32) {
        return (u32) (u16) ((arg0 * 2) + 1);
    }
    return (u32) (u16) native_arm7_fn_03806c38(0x1E00U, 0x7E - arg0, arg2, arg3);
}
