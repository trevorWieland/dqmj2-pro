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
extern u32 native_fn_ov001_022068a0();
extern u32 native_fn_ov001_0220723c();
u32 native_ov001_0220720c(u32 arg0, s8 arg1) {
    u32 temp_r4;
    void *temp_r1;

    temp_r4 = native_fn_ov001_022068a0();
    temp_r1 = temp_r4 + (native_fn_ov001_0220723c(arg0) << 5);
    M2C_FIELD(temp_r1, s8 *, 0x32) = arg1;
    M2C_FIELD(temp_r1, s8 *, 0x33) = 1;
    return 1U;
}
