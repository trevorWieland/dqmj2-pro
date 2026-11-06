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
extern u32 native_fn_0200708c();
extern u32 native_fn_02007110();
extern u32 native_fn_0203a554();
extern u32 native_fn_0203b638();
extern u8 native_data_020f4c84[];
extern u8 native_data_020f5508[];
u32 native_main_0203a838(u32 arg0, u32 arg1, void *arg2) {
    if (arg0 == M2C_FIELD(arg2, s32 *, 0x12C)) {
        goto block_2;
    }
    return arg0;
block_2:
    native_fn_0200708c(native_data_020f5508);
    if (M2C_FIELD(native_data_020f4c84, u32 *, 4) == 0) {
        goto block_4;
    }
    native_fn_0200708c(M2C_FIELD(native_data_020f4c84, u32 *, 4) + 0x4C8);
block_4:
    native_fn_0203a554(arg2);
    M2C_FIELD(arg2, s32 *, 0x12C) = 0;
    M2C_FIELD(arg2, s32 *, 0x130) = 0;
    M2C_FIELD(arg2, s8 *, 0x124) = 0;
    if ((s32) M2C_FIELD(arg2, s32 *, 0x120) <= 0) {
        goto block_6;
    }
    native_fn_0203b638(arg2);
    M2C_FIELD(arg2, s32 *, 0x120) = 0;
block_6:
    native_fn_02007110(native_data_020f5508);
    if (M2C_FIELD(native_data_020f4c84, u32 *, 4) != 0) {
        goto block_8;
    }
    return M2C_FIELD(native_data_020f4c84, u32 *, 4);
block_8:
    return native_fn_02007110(M2C_FIELD(native_data_020f4c84, u32 *, 4) + 0x4C8);
}
