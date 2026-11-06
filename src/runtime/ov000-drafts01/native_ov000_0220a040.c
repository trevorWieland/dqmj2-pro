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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u8 native_data_ov000_02238634[];
u32 native_ov000_0220a040(s32 arg0, s8 arg1) {
    s32 temp_r2;

    temp_r2 = (arg0 * 0x2C4) + (s32) native_data_ov000_02238634;
    M2C_FIELD(temp_r2, s8 *, 0x279) = 0;
    M2C_FIELD(temp_r2, s8 *, 0x2C0) = arg1;
    return 0U;
}
