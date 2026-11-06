typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_ov006_02201270(u32);
u32 native_ov006_022017ec(void *arg0) {
    if (M2C_FIELD(arg0, u16 *, 2) != 0) {
        return native_fn_ov006_02201270(0xAU);
    }
    return native_fn_ov006_02201270(0U);
}
