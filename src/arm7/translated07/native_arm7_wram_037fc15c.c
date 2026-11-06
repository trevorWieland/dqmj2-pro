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
extern u32 native_arm7_fn_037fdd00(void);
extern u32 native_arm7_fn_037fc180(u32, u32);
extern u32 native_arm7_data_038076f0;
u32 native_arm7_wram_037fc15c(void) {
    native_arm7_fn_037fdd00();
    return native_arm7_fn_037fc180(M2C_FIELD(&native_arm7_data_038076f0, u32 *, 0x28), 0U);
}
