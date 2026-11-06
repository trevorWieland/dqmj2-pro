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
u32 native_main_0202c2f8(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0) = 0x1000;
    M2C_FIELD(arg0, s32 *, 0x14) = 0x1000;
    M2C_FIELD(arg0, s32 *, 4) = 0;
    M2C_FIELD(arg0, s32 *, 0x30) = (s32) ((0 - M2C_FIELD(arg1, s32 *, 0x24)) * M2C_FIELD(arg1, u16 *, 0x2C) * 0x10);
    M2C_FIELD(arg0, s32 *, 0x34) = (s32) (M2C_FIELD(arg1, s32 *, 0x28) * M2C_FIELD(arg1, u16 *, 0x2E) * 0x10);
    M2C_FIELD(arg0, s32 *, 0x10) = 0;
    return (u32) arg0;
}
