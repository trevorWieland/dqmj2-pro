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
extern u8 native_data_020f6028[];
u32 native_main_0203d1f0(void) {
    if ((u16) ((u32) M2C_FIELD(native_data_020f6028, u32 *, 0xC) >> 0x10) == (u16) (((u8) M2C_FIELD(native_data_020f6028, u32 *, 0xC) * ~(u8) ((u32) M2C_FIELD(native_data_020f6028, u32 *, 0xC) >> 8)) + 0x7B)) {
        return 1U;
    }
    return 0U;
}
