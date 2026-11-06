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
extern void ** native_fn_02049ad0(s32);
extern u32 native_fn_02049f4c(void **);
extern u32 native_fn_0204a04c(void *arg0, u32 arg1, u32 arg2, u32 arg3);
extern u32 native_fn_02085270(void *arg0, s16 arg1, s16 arg2);
u32 native_main_020c9a3c(s32 arg0, u32 arg1, u32 arg2, u32 arg3, s16 arg4) {
    u8 *temp_r4;
    void **temp_r0;

    temp_r0 = native_fn_02049ad0(arg0);
    temp_r4 = M2C_FIELD(*temp_r0, u8 **, 4);
    native_fn_02049f4c(temp_r0);
    native_fn_0204a04c(temp_r4, arg1, arg2, arg3);
    return native_fn_02085270(temp_r4 + 0x3C, arg4, 0);
}
