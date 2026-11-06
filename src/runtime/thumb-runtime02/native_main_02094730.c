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
extern u32 native_fn_020946ec();
extern u32 native_fn_02094818();
u32 native_main_02094730(u8 arg0) {
    u32 temp_r4;
    u32 temp_r6;
    u32 var_r0;

    temp_r4 = native_fn_020946ec(1);
    var_r0 = native_fn_020946ec(0x10);
    temp_r6 = var_r0;
    M2C_FIELD(temp_r4, u8 *, 9) = arg0;
    if ((u32) arg0 < 0x10U) {
        var_r0 = (u32) M2C_FIELD(temp_r4, u8 *, 0x16);
        if ((u32) arg0 > var_r0) {
            M2C_FIELD(temp_r4, u8 *, 0x16) = arg0;
            if ((u32) arg0 > 7U) {
                M2C_FIELD(temp_r4, s8 *, 0x15) = (s8) native_fn_02094818(M2C_FIELD(temp_r6, u8 *, 0xD0D));
                var_r0 = (u32) M2C_FIELD((temp_r6 + (M2C_FIELD(temp_r6, u8 *, 0xD13) * 4)), u8 *, 0x444);
                M2C_FIELD(temp_r4, s8 *, 0x14) = (s8) var_r0;
            }
        }
    }
    return var_r0;
}
