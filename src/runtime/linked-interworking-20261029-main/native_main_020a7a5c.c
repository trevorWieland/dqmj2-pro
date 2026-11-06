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
extern u32 native_fn_0201b248();
extern u32 native_fn_020a64d4();
extern u32 native_fn_020a6550();
extern u32 native_fn_020a6d84();
extern u32 native_fn_020a771c();
extern u32 native_fn_020a7744();
extern u32 native_fn_020a7794();
extern u32 native_fn_020a7814();
extern u32 native_fn_020a7858();
extern u8 native_data_020e0370[];
u32 native_main_020a7a5c(u32 arg0, u8 *arg1, s32 arg2) {
    u32 temp_r0;
    u32 temp_r4;
    u32 temp_r7_2;
    u8 temp_r7;
    s32 spC;
    u16 sp8;
    u32 sp4;

    if (arg2 < 1) {
        return 0U;
    }
    temp_r7 = *arg1;
    temp_r0 = native_fn_020a771c(temp_r7);
    sp4 = temp_r0;
    if (arg2 < (s32) temp_r0) {
        return 0U;
    }
    if ((0x40 & temp_r7) && (native_fn_020a7794(arg0, arg1 + sp4, arg2 - sp4) == 0)) {
        return 0U;
    }
    if ((0x80 & temp_r7) && (native_fn_020a7744(arg1 + sp4, arg2 - sp4) == 0)) {
        return 0U;
    }
    if (native_fn_0201b248(arg1 + 1, native_data_020e0370, 4) == 0) {
        return -1U;
    }
    native_fn_020a7814(arg0, arg1, arg2, &spC, &sp8);
    temp_r7_2 = native_fn_020a64d4(arg0, spC, sp8);
    if (native_fn_020a6550() != 0) {
        return -2U;
    }
    temp_r4 = native_fn_020a7858(arg0, temp_r7_2, arg1, arg2, 1);
    native_fn_020a6d84(arg0, temp_r7_2);
    return temp_r4;
}
