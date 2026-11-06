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
extern u32 native_arm7_fn_037fba94(u32, u32, u32, u32);
extern u32 native_arm7_data_027fffe0;
extern u32 native_arm7_data_037fbbec;
u32 native_arm7_wram_037fbbcc(u32 arg0) {
    return native_arm7_fn_037fba94(arg0, (u32) &native_arm7_data_027fffe0, (u32) &native_arm7_data_037fbbec, 0U);
}
