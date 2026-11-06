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
extern u8 native_data_021c72a0[];
u32 native_main_02083d4c(void) {
    M2C_FIELD(native_data_021c72a0, s32 *, 0x3C) = 0;
    M2C_FIELD(native_data_021c72a0, s32 *, 0x20) = 0;
    M2C_FIELD(native_data_021c72a0, s32 *, 0x1C) = 0;
    M2C_FIELD(native_data_021c72a0, s32 *, 0x58) = 0;
    M2C_FIELD(native_data_021c72a0, s32 *, 0x54) = 0;
    M2C_FIELD(native_data_021c72a0, s8 *, 3) = 7;
    M2C_FIELD(native_data_021c72a0, s8 *, 4) = 0xD;
    M2C_FIELD(native_data_021c72a0, s16 *, 6) = 0xC;
    M2C_FIELD(native_data_021c72a0, s16 *, 0x12) = 0x64;
    M2C_FIELD(native_data_021c72a0, s16 *, 0x16) = 0xC;
    M2C_FIELD(native_data_021c72a0, s8 *, 2) = 0xE;
    M2C_FIELD(native_data_021c72a0, s8 *, 1) = 2;
    M2C_FIELD(native_data_021c72a0, u8 *, 0) = 2;
    return (u32) native_data_021c72a0;
}
