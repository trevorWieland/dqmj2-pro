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
extern u32 native_fn_020a1608();
extern u32 native_fn_020a2290();
extern u32 native_fn_020a2394();
extern u32 native_fn_020a3d70();
extern u32 native_fn_020a3d7c();
extern u32 native_fn_020b6c90();
u32 native_main_020a1878(void) {
    u32 temp_r4;
    u32 var_r5;

    var_r5 = 1;
    if (M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0x15) == 3) {
        if (M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0xD) != 0) {
            native_fn_020a2394();
        }
        native_fn_0209f130(6, 0xFFFEC5D2);
        return 0U;
    }
    temp_r4 = native_fn_020a3d70();
    M2C_FIELD(temp_r4, u8 *, 0x14) = (u8) M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0xD);
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x208) = 0;
    if (M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x19C) != 0) {
        native_fn_020b6c90(M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x19C));
        M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x19C) = 0;
    }
    if (M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0xD) != 0) {
        native_fn_020a2290();
    } else {
        native_fn_020a3d7c(4);
        var_r5 = native_fn_020a1608(0);
    }
    return var_r5;
}
