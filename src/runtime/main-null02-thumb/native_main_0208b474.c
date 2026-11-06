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
extern u8 native_data_021cfcb8[];
u32 native_main_0208b474(void *arg0) {
    u8 *var_r0;

    var_r0 = native_data_021cfcb8;
    if (M2C_FIELD(native_data_021cfcb8, u8 *(**)(void *, void *, void *, u16), 0x28) != NULL) {
        var_r0 = M2C_FIELD(native_data_021cfcb8, u8 *(**)(void *, void *, void *, u16), 0x28)(arg0 + 0x1E, arg0 + 0x18, arg0 + 0x2C, M2C_FIELD(arg0, u16 *, 6));
    }
    return (u32) var_r0;
}
