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

u32 native_arm7_wram_037ff940(void *arg0) {
    return (u32) (M2C_FIELD(arg0, u8 *, 3) << 0x1F) >> 0x1F;
}
