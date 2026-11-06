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
extern u32 native_fn_02008e0c();
extern u32 native_fn_0201b248();
extern u32 native_fn_02091a68();
extern u32 native_fn_02091afc();
u32 native_main_02091b94(void *arg0, s32 arg1) {
    u8 sp0[20];

    native_fn_02008e0c(arg0 + 0x3A4, arg0 + 0x3FC, 0x58);
    native_fn_02091a68(arg0, &sp0, 1);
    native_fn_02008e0c(arg0 + 0x3FC, arg0 + 0x3A4, 0x58);
    if (native_fn_0201b248(arg1, &sp0, 0x10) != 0) {
        M2C_FIELD(arg0, s8 *, 0x455) = 9;
        return 0x455U;
    }
    native_fn_02008e0c(arg0 + 0x2EC, arg0 + 0x348, 0x5C);
    native_fn_02091afc(arg0, &sp0, 1);
    native_fn_02008e0c(arg0 + 0x348, arg0 + 0x2EC, 0x5C);
    if (native_fn_0201b248(arg1 + 0x10, &sp0, 0x14) != 0) {
        M2C_FIELD(arg0, s8 *, 0x455) = 9;
        return 0x455U;
    }
    M2C_FIELD(arg0, s8 *, 0x455) = 6;
    return 0x455U;
}
