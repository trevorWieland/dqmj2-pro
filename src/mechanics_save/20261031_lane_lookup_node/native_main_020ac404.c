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
extern u32 native_fn_020a929c(u32);
extern u32 native_fn_020aaf08(void **,void *);
extern u32 native_fn_020b0a50(void **,u32,void **);
extern u32 native_fn_020b0b48(void **,void *);
extern u32 native_fn_020b0ca8(void *);
extern u32 native_fn_020b2c88(s32 *,u32);
extern u8 native_data_020e0768[];
u32 native_main_020ac404(void **arg0, u32 arg1) {
    u32 var_r0;
    void *temp_r4;
    void *sp0;

    temp_r4 = *arg0;
    if (native_fn_020b0a50(arg0, arg1, &sp0) == 0) {
        native_fn_020b2c88((s32 *)arg0, (u32)native_data_020e0768);
        return 2U;
    }
    if (M2C_FIELD(sp0, s32 *, 0x14) == 0) {
        native_fn_020b2c88((s32 *)arg0, (u32)native_data_020e0768);
        return 2U;
    }
    var_r0 = native_fn_020aaf08(arg0,sp0);
    if (var_r0 == 0) {
        M2C_FIELD(sp0, s32 *, 0x18) = (s32)(M2C_FIELD(sp0, u32 *, 0x18) - 1U);
        if ((M2C_FIELD(temp_r4, s32 *, 0x100) == 0) && ((s32) M2C_FIELD(sp0, s32 *, 0x18) <= 0)) {
            native_fn_020a929c(M2C_FIELD(sp0, s32 *, 0x14));
            M2C_FIELD(sp0, s32 *, 0x14) = 0;
            if (native_fn_020b0ca8(sp0) != 0) {
                native_fn_020b0b48(arg0, sp0);
            }
        }
        var_r0 = 0;
    }
    return var_r0;
}
