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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
extern u8 native_data_020e3304[];
void native_main_02002d44(void) {
    M2C_FIELD(native_data_020e3304, s16 *, 0) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 2) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 4) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 6) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 8) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 0xA) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 0xC) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 0xE) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 0x10) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 0x12) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 0x14) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 0x16) = 0;
    M2C_FIELD(native_data_020e3304, s16 *, 0x18) = 0;
    M2C_FIELD((void *)0x04000240, s32 *, 0) = 0;
    M2C_FIELD((void *)0x04000240, s8 *, 4) = 0;
    M2C_FIELD((void *)0x04000240, s8 *, 5) = 0;
    M2C_FIELD((void *)0x04000240, s8 *, 6) = 0;
    M2C_FIELD((void *)0x04000240, s16 *, 8) = 0;
}
