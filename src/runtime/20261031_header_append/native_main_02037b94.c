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
extern u8 *native_fn_0202b784(u32 handle, u32 bytes, u32 alignment);
extern void native_fn_0202ba20(u32 list, u8 *record);
extern u32 native_fn_0202bba0(s32 *prefix, u32 node);
u32 native_main_02037b94(s32 *arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    u32 temp_r0_2;
    u8 *temp_r0;

    temp_r0 = native_fn_0202b784(*arg0, ((arg1 + 0x1F) & ~0x1F) + 0x20, 0x20);
    if (temp_r0 == NULL) {
        return 0U;
    }
    temp_r0_2 = native_fn_0202bba0(arg0 + 1, 0);
    M2C_FIELD(temp_r0, s32 *, 8) = arg1;
    M2C_FIELD(temp_r0, s32 *, 0xC) = arg2;
    M2C_FIELD(temp_r0, s32 *, 0x10) = arg3;
    M2C_FIELD(temp_r0, s32 *, 0x14) = arg4;
    native_fn_0202ba20(temp_r0_2, temp_r0);
    return (u32) (temp_r0 + 0x20);
}
