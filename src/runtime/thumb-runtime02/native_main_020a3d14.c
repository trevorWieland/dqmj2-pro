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
extern u32 native_fn_0209f130();
extern u32 native_fn_020a3d70();
u32 native_main_020a3d14(s32 arg0) {
    void *temp_r0;

    if (arg0 != 0) {
        return 1U;
    }
    if (M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0x15) != 3) {
        temp_r0 = (void *) native_fn_020a3d70();
        M2C_FIELD(temp_r0, u8 *, 0x17D) = (u8) (M2C_FIELD(temp_r0, u8 *, 0x17D) + 1);
    }
    if ((M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0x15) == 3) || ((u32) M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0x17D) >= 5U)) {
        native_fn_0209f130(6, 0xFFFEAE6C);
        return 0U;
    }
    return 1U;
}
