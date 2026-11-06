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
extern u32 native_fn_0207b244();
extern u32 native_fn_0207b460();
u32 native_ov000_022153bc(void *arg0, u32 arg1) {
    u8 sp0[64];
    u32 temp_r0;

    native_fn_0207b460(M2C_FIELD(arg0, s16 *, 0x18), M2C_FIELD(arg0, u8 *, 0x1A), arg0 + 0x7A, &sp0);
    temp_r0 = native_fn_0207b244(arg1, M2C_FIELD(arg0, s16 *, 0x26), &sp0);
    if (temp_r0 == 0x2710) {
        return (u32) M2C_FIELD(arg0, s16 *, 0x26);
    }
    if (temp_r0 != 0x2711) {
        return temp_r0;
    }
    return (u32) ((s32) ((M2C_FIELD(arg0, s16 *, 0x26) + 1) << 0xF) >> 0x10);
}
