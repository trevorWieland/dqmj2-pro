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
extern u32 native_fn_0207afec();
u32 native_ov001_0220ee3c(u32 arg0, u32 arg1, s32 arg2) {
    s32 temp_r1;
    u8 temp_r0;
    u8 temp_r4;

    temp_r4 = M2C_FIELD((void *) native_fn_0207afec(), u8 *, 0x1F);
    temp_r0 = M2C_FIELD((void *) native_fn_0207afec(arg0), u8 *, 0x20);
    if ((temp_r4 != arg2) && (temp_r0 != arg2)) {
        return arg1;
    }
    temp_r1 = arg1 * 5;
    return (u32) ((s32) (temp_r1 + ((u32) (temp_r1 >> 1) >> 0x1E)) >> 2);
}
