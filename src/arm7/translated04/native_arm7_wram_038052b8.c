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
extern u32 native_arm7_fn_037fe070(u32, u32, u32);
extern u32 native_arm7_fn_0380532c(u32);
extern u32 native_arm7_data_03809ee4;
extern u32 native_arm7_data_03809ef4;
u32 native_arm7_wram_038052b8(u32 arg0) {
    M2C_FIELD(&native_arm7_data_03809ee4, s32 *, 4) = 0;
    M2C_FIELD(&native_arm7_data_03809ee4, u32 *, 8) = arg0;
    native_arm7_fn_037fe070((u32) &native_arm7_data_03809ef4, 0U, 0xA4U);
    native_arm7_fn_0380532c(arg0);
    M2C_FIELD(&native_arm7_data_03809ee4, s8 *, 0) = 3;
    return (u32) &native_arm7_data_03809ee4;
}
