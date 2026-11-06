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
extern u64 native_fn_020a8ef8(void);
extern u32 native_fn_020b3b0c(const u8 *, const u8 *);
extern u32 native_fn_020b3c24(void *, void *, u32, u32, u32, u8 *, s32);
extern void native_fn_020b42a4(void *, ...);
extern u32 native_fn_020b4634(u32);
extern u32 native_fn_020b589c(u32);
u32 native_main_020b48c8(u8 *arg0, u8 *arg1, s32 arg2) {
    if (M2C_FIELD(arg0, s32 *, 0xC) != 3) {
        if (native_fn_020b4634((u32) arg0) != 0) {
            return 1U;
        }
        return 0U;
    }
    if (arg2 < 0x20) {
        if (native_fn_020b4634((u32) arg0) != 0) {
            return 1U;
        }
        return 0U;
    }
    if (native_fn_020b3b0c(arg1, arg0 + 0x68) == 0) {
        if (native_fn_020b4634((u32) arg0) != 0) {
            return 1U;
        }
        return 0U;
    }
    if (M2C_FIELD(M2C_FIELD(arg0, void **, 8), s32 *, 0x20) == 0) {
        if (native_fn_020b589c((u32) arg0) == 0) {
            return 0U;
        }
        native_fn_020b42a4(arg0);
        return 1U;
    }
    M2C_FIELD(arg0, s32 *, 0xC) = 4;
    if (native_fn_020b3c24(M2C_FIELD(arg0, void **, 8), arg0, M2C_FIELD(arg0, s32 *, 0), M2C_FIELD(arg0, u16 *, 4), (u32)native_fn_020a8ef8() - M2C_FIELD(arg0, s32 *, 0x8C), arg1 + 0x20, arg2 - 0x20) != 0) {
        return 1U;
    }
    return 0U;
}
