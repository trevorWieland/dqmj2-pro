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
extern u32 native_fn_020c8fa8();
extern u8 native_data_02101ae8[];
extern u8 native_data_021d64b8[];
u32 native_main_020c9294(s32 arg0) {
    if (((M2C_FIELD((void *) native_fn_020c8fa8(), s8 *, 0x10) == 1) || (M2C_FIELD((void *) native_fn_020c8fa8(), s8 *, 0x10) == 2)) && (arg0 != 0)) {
        M2C_FIELD(M2C_FIELD(native_data_021d64b8, void **, 0x10), s32 *, 0x7C) = (s32) (M2C_FIELD(M2C_FIELD(native_data_021d64b8, void **, 0x10), s32 *, 0x7C) | 2);
    } else {
        M2C_FIELD(M2C_FIELD(native_data_021d64b8, void **, 0x10), s32 *, 0x7C) = (s32) (M2C_FIELD(M2C_FIELD(native_data_021d64b8, void **, 0x10), s32 *, 0x7C) & ~2);
    }
    M2C_FIELD(native_data_02101ae8, s32 *, 0xC84) = 1;
    return (u32) native_data_02101ae8;
}
