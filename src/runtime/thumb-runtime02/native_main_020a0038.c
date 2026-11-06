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
extern u32 native_fn_020a304c();
extern u32 native_fn_020a3a48();
extern u32 native_fn_020a3a4c();
extern u32 native_fn_020a3d70();
extern u32 native_fn_020a68ec();
extern u32 native_fn_020b45a0();
extern u32 native_fn_020b5f38();
extern u32 native_fn_020b6c08();
u32 native_main_020a0038(void *arg0) {
    s32 var_r4;
    u32 temp_r0;
    u32 temp_r4;

    if (M2C_FIELD(arg0, u8 *, 0) == 0) {
        temp_r4 = native_fn_020a3d70();
        native_fn_020a68ec(M2C_FIELD(temp_r4, s32 *, 0xE4), native_fn_020b5f38(M2C_FIELD(arg0, s32 *, 4), 0, 0), M2C_FIELD(arg0, u16 *, 2), M2C_FIELD(arg0, s32 *, 8));
        if (native_fn_020a304c() != 0) {
            return 2U;
        }
    }
    var_r4 = 0;
loop_4:
    temp_r0 = native_fn_020b6c08(native_fn_020b45a0(*M2C_FIELD((void *) native_fn_020a3d70(), s32 **, 4)), M2C_FIELD(arg0, s32 *, 8), M2C_FIELD(arg0, u8 *, 0), native_fn_020a3a48, native_fn_020a3a4c, arg0);
    if ((temp_r0 != 0) && (temp_r0 == 3)) {
        var_r4 += 1;
        if (var_r4 < 5) {
            goto loop_4;
        }
    }
    return temp_r0;
}
