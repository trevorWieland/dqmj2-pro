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
u32 native_ov001_02212f14(void *arg0, u32 arg1) {
    M2C_FIELD(arg0, u32 *, 0x10) = (u32) M2C_FIELD(arg0, u32 *, 0x2C);
    M2C_FIELD(arg0, u32 *, 0x2C) = arg1;
    switch (arg1) {
    case 0:
    case 1:
        break;
    default:
        break;
    case 2:
        M2C_FIELD(arg0, s8 *, 0x24) = 0;
        break;
    case 3:
        M2C_FIELD(arg0, s32 *, 0x38) = 6;
        M2C_FIELD(arg0, s8 *, 0x24) = 0;
        break;
    case 4:
        M2C_FIELD(arg0, s8 *, 0x24) = 0x14;
        break;
    }
    M2C_FIELD(arg0, s32 *, 0x34) = 0;
    return (u32) arg0;
}
