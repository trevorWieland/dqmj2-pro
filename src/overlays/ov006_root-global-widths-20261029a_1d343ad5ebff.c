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
extern u8 native_data_ov006_0220f614[];
u32 native_ov006_021dfe74(s32 arg0, s8 arg1, s16 arg2) {
    void *temp_r0;

    *(u32 *)(native_data_ov006_0220f614 + (arg0 * 0x10)) = 1;
    temp_r0 = native_data_ov006_0220f614 + (arg0 * 0x10);
    M2C_FIELD(temp_r0, s8 *, 8) = arg1;
    M2C_FIELD(temp_r0, s16 *, 0xA) = arg2;
    return (u32) temp_r0;
}
