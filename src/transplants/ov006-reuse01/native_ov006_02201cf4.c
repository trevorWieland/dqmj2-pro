typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_ov006_022017a8(void);
extern u32 native_fn_ov006_02201270(u32);
u32 native_ov006_02201cf4(void) {
    u32 var_r0;

    var_r0 = native_fn_ov006_022017a8();
    if (var_r0 == 0) {
        var_r0 = native_fn_ov006_02201270(0xAU);
    }
    return var_r0;
}
