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
extern u32 native_fn_02008c14();
extern u32 native_fn_02028dac();
extern u32 native_fn_020297e0();
extern u32 native_fn_02029950();
extern u32 native_fn_0204124c();
extern u32 native_fn_ov000_02211610();
extern u32 native_fn_ov000_02212148();
extern u8 native_data_ov000_0224157c[];
u32 native_ov000_02212180(void) {
    s32 var_r5;
    u8 *var_r6;

    var_r5 = 0;
    var_r6 = native_data_ov000_0224157c;
    do {
        if (((s32) M2C_FIELD(var_r6, s16 *, 0) > 0) && (M2C_FIELD(var_r6, u8 *, 0xA) != 0)) {
            native_fn_0204124c(var_r6 + 0x14);
            native_fn_02029950(var_r6 + 0x14);
            native_fn_020297e0(var_r6 + 0x14);
            if (native_fn_02028dac(var_r6 + 0x14) != 0) {
                M2C_FIELD(var_r6, u8 *, 0xA) = 0U;
            }
            native_fn_ov000_02211610(M2C_FIELD(var_r6, s16 *, 0), M2C_FIELD(var_r6, s16 *, 2));
        }
        var_r5 += 1;
        var_r6 += 0x168;
    } while (var_r5 < 0x18);
    native_fn_ov000_02212148();
    native_fn_02008c14(0, native_data_ov000_0224157c, 0x21C0);
    return 0U;
}
