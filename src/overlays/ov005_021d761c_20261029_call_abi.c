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
#define NULL ((void *)0)
extern u32 native_fn_ov005_021d75f8(void *);
extern u32 native_fn_ov005_021d8788();
u32 native_ov005_021d761c(void *arg0, s32 arg1, s32 arg2) {
    if (arg2 == 0) {
        return (u32) arg0;
    }
    switch (arg1) {
    case 0x81:
        return (u32) arg0;
    default:
        return native_fn_ov005_021d75f8(arg0);
    case 0x1:
    case 0x3:
    case 0x4:
    case 0x5:
    case 0x6:
        return native_fn_ov005_021d75f8(arg0);
    case 0xE:
        M2C_FIELD(arg0, s32 *, 0x50F0) = 5;
        return native_fn_ov005_021d75f8(arg0);
    case 0x26:
    case 0x7:
    case 0x8:
    case 0xB:
    case 0xD:
    case 0x1E:
        return native_fn_ov005_021d75f8(arg0);
    case 0xC:
        if ((arg2 == 1) || (((u32)arg2 - 0xBU) <= 1U)) {
            M2C_FIELD(arg0, s32 *, 0x50F0) = 5;
            return native_fn_ov005_021d8788(arg0, 3);
        }
        return native_fn_ov005_021d75f8(arg0);
    case 0x80:
        return native_fn_ov005_021d75f8(arg0);
    case 0xF:
        return (u32) arg0;
    }
}
