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
extern u32 native_fn_020404f0();
extern u32 native_fn_0205bf4c();
extern u32 native_fn_0205bf5c();
extern u32 native_fn_ov000_021e0f58();
u32 native_ov000_021e0f84(void) {
    u32 temp_r0;
    u32 var_r4;

    var_r4 = 0;
    if (native_fn_ov000_021e0f58() != 0) {
        temp_r0 = native_fn_0205bf4c();
        if (temp_r0 == 0x2A2F) {
            native_fn_0205bf5c(0x2A30);
            native_fn_020404f0(0x1E);
            var_r4 = 1;
        } else if (temp_r0 == 0x4650) {
            native_fn_0205bf5c(0);
            native_fn_020404f0(0x1E);
            var_r4 = 1;
        }
    }
    return var_r4;
}
