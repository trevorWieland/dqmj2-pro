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
extern u32 native_fn_020875b4();
u32 native_main_02049f4c(void **arg0) {
    void *temp_r0;
    void *temp_r0_2;

    temp_r0_2 = *arg0;
    if (temp_r0_2 == NULL) {
        return (u32) temp_r0_2;
    }
    temp_r0 = M2C_FIELD(temp_r0_2, void **, 4);
    return native_fn_020875b4(temp_r0, M2C_FIELD(temp_r0, u8 *, 0x5E), M2C_FIELD(temp_r0, u8 *, 0x5F), M2C_FIELD(temp_r0, u8 *, 0x5C), (s32) M2C_FIELD(temp_r0, u8 *, 0x5D), M2C_FIELD(temp_r0, s32 *, 0x58));
}
