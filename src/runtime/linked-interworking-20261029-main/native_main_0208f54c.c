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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_0208da88();
u32 native_main_0208f54c(void *arg0) {
    void *temp_r4;
    u32 temp_r5;
    u32 temp_r6;

    temp_r4 = M2C_FIELD(arg0, void **, 0x64);
    temp_r6 = native_fn_02007ff4();
    temp_r5 = M2C_FIELD(temp_r4, u32 *, 0xF8);
    if (temp_r5 != 0) {
        M2C_FIELD(temp_r4, u32 *, 0xF8) = 0U;
        native_fn_0208da88(temp_r5);
    }
    native_fn_02008008(temp_r6);
    return temp_r5;
}
