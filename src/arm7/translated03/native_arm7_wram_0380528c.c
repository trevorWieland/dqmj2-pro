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
extern u32 native_arm7_data_03809edc;
u32 native_arm7_wram_0380528c(s32 arg0) {
    if (arg0 <= 0xF) {
        M2C_FIELD(&native_arm7_data_03809edc, s32 *, 4) = arg0;
        M2C_FIELD(&native_arm7_data_03809edc, u32 *, 0) = 0;
    }
    return (u32) arg0;
}
