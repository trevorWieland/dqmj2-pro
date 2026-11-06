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
extern u32 native_fn_0203d294();
extern u32 native_fn_0207b244();
extern u32 native_fn_ov001_021dbd30();
extern u32 native_fn_ov001_021dbec8();
u32 native_ov001_02218e78(void *arg0) {
    u32 temp_r4_2;
    u32 temp_r5;
    void *temp_r4;

    temp_r4 = M2C_FIELD(arg0, void **, 0);
    temp_r5 = native_fn_ov001_021dbd30(temp_r4);
    temp_r4_2 = native_fn_ov001_021dbec8(temp_r4);
    if (((s32) temp_r5 < (s32) native_fn_0207b244(M2C_FIELD(arg0, s32 *, 0xC), temp_r5, M2C_FIELD(temp_r4, s32 *, 0x1E8) + 0x46)) && ((temp_r4_2 != 0) || ((s32) native_fn_0203d294(0xA) < 9))) {
        return 1U;
    }
    return 0U;
}
