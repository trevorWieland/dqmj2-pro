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
extern u32 native_fn_0207b20c();
extern u32 native_fn_0207b228();
extern u32 native_fn_ov001_021dbf98();
u32 native_ov001_021e1950(u32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    u32 temp_r2;
    u32 temp_r4;

    temp_r4 = native_fn_0207b20c();
    temp_r2 = native_fn_0207b228(arg0);
    if ((temp_r4 == 0) || ((arg2 == 0) && (temp_r2 == M2C_FIELD((arg1 + temp_r4), s8 *, 0x22C)))) {
        return 0U;
    }
    return native_fn_ov001_021dbf98(arg1, temp_r4, temp_r2, 0, arg3);
}
