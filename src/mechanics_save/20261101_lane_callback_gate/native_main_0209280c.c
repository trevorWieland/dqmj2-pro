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
extern u32 native_fn_0208d820(void *);
extern u32 native_fn_02092778();
extern u32 native_fn_02092ffc(u32 arg0);
extern u32 native_fn_020936bc(u32 arg0);
u32 native_main_0209280c(void *arg0) {
    void *temp_r4;

    temp_r4 = M2C_FIELD(arg0, void **, 0xC);
    if ((M2C_FIELD(arg0, u8 *, 8) != 4) && (native_fn_0208d820(arg0) != 0)) {
        return 1U;
    }
    M2C_FIELD(temp_r4, s8 *, 0x455) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x1D4) = 0;
    M2C_FIELD(temp_r4, s8 *, 0x454) = 0;
    native_fn_020936bc((u32) (temp_r4 + 0x2EC));
    native_fn_02092ffc((u32) (temp_r4 + 0x3A4));
    return native_fn_02092778(arg0);
}
