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
u32 native_main_020ac480(u32 arg0, void *arg1, s32 arg2) {
    s32 temp_r0;
    s32 temp_r0_2;
    s32 *temp_r1;
    s32 *temp_r3;

    temp_r3 = M2C_FIELD(arg1, s32 **, 8);
    if ((temp_r3 != NULL) && (temp_r0 = *temp_r3, (temp_r0 > arg2))) {
        *temp_r3 = temp_r0 - 1;
    } else {
        temp_r1 = M2C_FIELD(arg1, s32 **, 0xC);
        if (temp_r1 != NULL) {
            temp_r0_2 = *temp_r1;
            if (temp_r0_2 > arg2) {
                *temp_r1 = temp_r0_2 - 1;
            }
        }
    }
    return 1U;
}
