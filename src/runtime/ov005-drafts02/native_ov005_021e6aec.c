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
extern u32 native_fn_020cf590();
void native_ov005_021e6aec(void *arg0) {
    s16 sp2;
    u8 sp0;

    native_fn_020cf590(M2C_FIELD(arg0, s16 *, 0x18), &sp2, &sp0);
    M2C_FIELD(arg0, s16 *, 0x18) = sp2;
    M2C_FIELD(arg0, u8 *, 0x1A) = sp0;
    return;
}
