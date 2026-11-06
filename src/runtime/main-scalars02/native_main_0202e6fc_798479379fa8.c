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
extern u8 native_data_020ee010[];
u32 native_main_0202e6fc(u32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    *(u32 *)(native_data_020ee010 + (arg0 * 4)) = (0x3FF & (arg1 >> 3)) | ((u32) ((arg2 >> 3) << 0x16) >> 0xC) | ((u32) ((arg3 >> 3) << 0x16) >> 2) | (arg0 << 0x1E);
    return arg0;
}
