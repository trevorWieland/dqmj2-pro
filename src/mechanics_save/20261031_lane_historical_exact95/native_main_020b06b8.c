#define NULL ((void *)0)
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
extern void * native_fn_020b03c4(u32,u32,u32);
u32 native_main_020b06b8(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u8 *temp_r0;

    temp_r0 = native_fn_020b03c4(arg3, arg0, arg1);
    if (temp_r0 != NULL) {
        *(u32 *)temp_r0 = 0x6A;
    }
    return (u32) temp_r0;
}
