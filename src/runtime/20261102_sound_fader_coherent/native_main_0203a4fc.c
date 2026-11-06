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
extern u32 native_fn_020379c4(void *, s32, s32);
extern u32 native_fn_0203a554(void *);
u32 native_main_0203a4fc(void *arg0, u32 arg1) {
    if (((s32) (M2C_FIELD(arg0, u32 *, 0x110) << 0x1E) >> 0x1F) == 0) {
        return native_fn_0203a554(arg0);
    }
    if (arg1 == 0) {
        return native_fn_0203a554(arg0);
    }
    native_fn_020379c4((u8 *)arg0 + 0xE8, 0, (s32) arg1);
    M2C_FIELD(arg0, s32 *, 0x110) = (s32) (M2C_FIELD(arg0, s32 *, 0x110) | 8);
    M2C_FIELD(arg0, s32 *, 0x150) = 0;
    return 0U;
}
