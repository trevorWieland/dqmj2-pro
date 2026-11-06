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
u32 native_ov000_021f9558(void *arg0, s32 arg1) {
    s16 temp_r2;

    temp_r2 = 0xC0 - ((arg1 + 1) * 0x28);
    if ((s32) M2C_FIELD(arg0, s16 *, 0) < 0) {
        M2C_FIELD(arg0, s16 *, 0) = 0;
    }
    if ((s32) M2C_FIELD(arg0, s16 *, 0) > 0xD8) {
        M2C_FIELD(arg0, s16 *, 0) = 0xD8;
    }
    if ((s32) M2C_FIELD(arg0, s16 *, 2) < 0x18) {
        M2C_FIELD(arg0, s16 *, 2) = 0x18;
    }
    if ((s32) M2C_FIELD(arg0, s16 *, 2) > (s32) temp_r2) {
        M2C_FIELD(arg0, s16 *, 2) = temp_r2;
    }
    return (u32) arg0;
}
