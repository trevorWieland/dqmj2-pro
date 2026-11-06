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
extern u8 native_data_ov005_021e78cc[];
u32 native_ov005_021d9124(void) {
    u16 temp_r0;

    temp_r0 = M2C_FIELD(*(u32 *)native_data_ov005_021e78cc, u16 *, 0x5206);
    if (temp_r0 == 0) {
        return (u32) temp_r0;
    }
    return (u32) (u16) (temp_r0 | (1 << M2C_FIELD(*(u32 *)native_data_ov005_021e78cc, u16 *, 0x5204)));
}
