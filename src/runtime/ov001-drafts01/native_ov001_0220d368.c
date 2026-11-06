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
extern u32 native_fn_02065d88();
u32 native_ov001_0220d368(void) {
    u8 temp_r0;

    temp_r0 = M2C_FIELD((void *) native_fn_02065d88(), u8 *, 0x28);
    switch ((s32) temp_r0) {
    case 42:
    case 1:
    case 13:
        return 1U;
    case 2:
    case 14:
        return 2U;
    case 35:
    case 15:
        return 3U;
    case 39:
    case 36:
    case 16:
        return 4U;
    case 40:
    case 37:
    case 17:
        return 5U;
    case 41:
    case 38:
    case 18:
        return 6U;
    default:
        return 0U;
    }
}
