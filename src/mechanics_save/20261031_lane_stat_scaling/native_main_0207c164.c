typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_02026144(s32, s32);
u32 native_main_0207c164(s32 value, s32 divisor) {
    s16 ratio;
    ratio = (s16)native_fn_02026144((s16)value * 100, divisor);
    return ratio < 20;
}
