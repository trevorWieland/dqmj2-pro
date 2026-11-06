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
extern u32 native_fn_0207afec();
u32 native_ov001_021d9e20(u8 *indices, s32 count) {
    s32 first;
    s32 second;
    u32 swaps;
    u8 priority;
    u8 original;

    swaps = 0;
    first = 0;
    if (count > 0) {
        do {
            second = first + 1;
            if (second < count) {
                do {
                    priority = M2C_FIELD((void *) native_fn_0207afec(*(indices + first)), u8 *, 0x24);
                    if ((s32) priority > (s32) M2C_FIELD((void *) native_fn_0207afec(*(indices + second)), u8 *, 0x24)) {
                        original = *(indices + first);
                        swaps += 1;
                        *(indices + first) = *(indices + second);
                        *(indices + second) = original;
                    }
                    second += 1;
                } while (second < count);
            }
            first += 1;
        } while (first < count);
    }
    return swaps;
}
