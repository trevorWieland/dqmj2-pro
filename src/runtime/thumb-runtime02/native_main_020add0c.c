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
extern u32 native_fn_020acbcc();
extern u32 native_fn_020b2b24();
extern u32 native_fn_020b2c6c();
extern u8 native_data_020e0c2c[];
u32 native_main_020add0c(void **arg0) {
    s32 sp0;
    u32 var_r0;
    void *temp_r4;

    temp_r4 = *arg0;
    var_r0 = native_fn_020b2b24(arg0, M2C_FIELD(temp_r4, s32 *, 0x1F0), &sp0);
    if (var_r0 == 0) {
        if (sp0 == 4) {
            native_fn_020b2c6c(arg0, 0x107, native_data_020e0c2c);
            native_fn_020acbcc(arg0, 4, 1);
            return 4U;
        }
        if (sp0 == 0) {
            return 0U;
        }
        M2C_FIELD(temp_r4, s32 *, 0x1F4) = 2;
        var_r0 = 0;
        
        return var_r0;
    }
    return var_r0;
}
