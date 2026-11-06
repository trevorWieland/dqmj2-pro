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
extern u32 native_fn_020a929c(u32);
extern u32 native_fn_020b3a58(u8 *, const u8 *);
extern u32 native_fn_020b3b0c(const u8 *, const u8 *);
extern u32 native_fn_020b4634(u32 arg0);
extern u32 native_fn_020b557c(u32 arg0, u32 arg1, u32 arg2, u32 arg3);
u32 native_main_020b4834(void *arg0, u8 *arg1, s32 arg2) {
    u8 sp0[32];

    if (M2C_FIELD(arg0, s32 *, 0xC) != 0) {
        if (native_fn_020b4634((u32) arg0) != 0) {
            return 1U;
        }
        return 0U;
    }
    if (arg2 < 0x40) {
        if (native_fn_020b4634((u32) arg0) != 0) {
            return 1U;
        }
        return 0U;
    }
    if (native_fn_020b3b0c(arg1, (u8 *)arg0 + 0x68) == 0) {
        if (native_fn_020b4634((u32) arg0) != 0) {
            return 1U;
        }
        return 0U;
    }
    native_fn_020b3a58(sp0, arg1 + 0x20);
    if (native_fn_020b557c((u32) arg0, (u32) sp0, M2C_FIELD(arg0, u32 *, 0x38), M2C_FIELD(arg0, u32 *, 0x3C)) == 0) {
        return 0U;
    }
    if (M2C_FIELD(arg0, u32 *, 0x38) != 0) {
        native_fn_020a929c(M2C_FIELD(arg0,u32 *,0x38));
        M2C_FIELD(arg0, u32 *, 0x38) = 0U;
    }
    M2C_FIELD(arg0, s32 *, 0xC) = 1;
    return 1U;
}
