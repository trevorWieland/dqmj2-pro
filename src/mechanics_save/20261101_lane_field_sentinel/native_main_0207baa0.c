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
extern u32 native_fn_02044cdc(u32);
extern u32 native_fn_0207afec(s32);
extern u32 native_fn_0207b974(u32, s32, s32, s32, u32);
extern u32 native_fn_0207ba64(u32, s32);
extern u32 native_fn_0207d198(const u8 *, u32, u32);
u32 native_main_0207baa0(u32 arg0, u32 arg1, s32 arg2, const u8 *arg3, s32 arg4, s32 arg5) {
    s16 var_r2;
    u32 temp_r5;

    if (arg4 == 0) {
        var_r2 = M2C_FIELD((void *) native_fn_0207afec((s32)arg0), s16 *, 0x10);
    } else {
        var_r2 = M2C_FIELD((void *) native_fn_0207afec((s32)arg0), s16 *, 0x14);
    }
    if (var_r2 != 0x2710) {
        goto block_5;
    }
    return -1U;
block_5:
    if (var_r2 != 0x2711) {
        goto block_7;
    }
    return -2U;
block_7:
    if (var_r2 != 0x2713) {
        goto block_9;
    }
    return -3U;
block_9:
    if (var_r2 != 0x2716) {
        goto block_11;
    }
    return -4U;
block_11:
    if (var_r2 != 0x2712) {
        goto block_13;
    }
    return -5U;
block_13:
    temp_r5 = native_fn_0207b974(arg0, arg2, arg4, arg5, 0);
    return native_fn_0207d198(arg3, arg0, native_fn_0207ba64(temp_r5, native_fn_02044cdc(arg1)));
}
